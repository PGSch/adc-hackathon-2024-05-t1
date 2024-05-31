import logging
import re
import ast
import os
import sys
from openai import OpenAI
import pytest
import subprocess

color_prefix_by_role = {
    "system": "\033[0m",  # gray
    "user": "\033[0m",  # gray
    "assistant": "\033[92m",  # green
}


def unittest_flow(
    function_to_test: str,
    function_filename: str,  # Ensure this is passed correctly
    unit_test_package: str = "pytest",
    approx_min_cases_to_cover: int = 7,
    print_text: bool = False,
    explain_model: str = "gpt-3.5-turbo",
    plan_model: str = "gpt-3.5-turbo",
    execute_model: str = "gpt-3.5-turbo",
    temperature: float = 0.3,
    reruns_if_fail: int = 1,
    stream: bool = False,
) -> str:
    client = OpenAI()

    # Helper functions
    def print_messages(messages, color_prefix_by_role=color_prefix_by_role):
        for message in messages:
            role = message["role"]
            color_prefix = color_prefix_by_role[role]
            content = message["content"]
            print(f"{color_prefix}\n[{role}]\n{content}")

    def print_message_assistant(content, color_prefix_by_role=color_prefix_by_role):
        role = "assistant"
        color_prefix = color_prefix_by_role[role]
        print(f"{color_prefix}\n[{role}]\n{content}")

    def print_message_delta(delta, color_prefix_by_role=color_prefix_by_role):
        if "role" in delta:
            role = delta["role"]
            color_prefix = color_prefix_by_role[role]
            print(f"{color_prefix}\n[{role}]\n", end="")
        elif "content" in delta:
            content = delta["content"]
            print(content, end="")
        else:
            pass

    # Step 1: Generate an explanation of the function
    explain_system_message = {
        "role": "system",
        "content": "You are a world-class Python developer with an eagle eye for unintended bugs and edge cases. You carefully explain code with great detail and accuracy. You organize your explanations in markdown-formatted, bulleted lists.",
    }
    explain_user_message = {
        "role": "user",
        "content": f"""Please explain the following Python function. Review what each element of the function is doing precisely and what the author's intentions may have been. Organize your explanation as a markdown-formatted, bulleted list.

```python
{function_to_test}
```""",
    }
    explain_messages = [explain_system_message, explain_user_message]
    if print_text:
        print_messages(explain_messages)

    explanation_response = client.chat.completions.create(
        model=explain_model,
        messages=explain_messages,
        temperature=temperature,
        stream=False,
    )
    explanation = ""
    if stream:
        for chunk in explanation_response:
            delta = chunk.choices[0].delta
            if print_text:
                print_message_delta(delta)
            if "content" in delta:
                explanation += delta["content"]
    else:
        explanation = explanation_response.choices[0].message.content
        if print_text:
            print_message_assistant(explanation)
    explain_assistant_message = {"role": "assistant", "content": explanation}

    # Step 2: Generate a plan to write a unit test
    plan_user_message = {
        "role": "user",
        "content": f"""A good unit test suite should aim to:
- Test the function's behavior for a wide range of possible inputs
- Test edge cases that the author may not have foreseen
- Take advantage of the features of `{unit_test_package}` to make the tests easy to write and maintain
- Be easy to read and understand, with clean code and descriptive names
- Be deterministic, so that the tests always pass or fail in the same way

To help unit test the function above, list diverse scenarios that the function should be able to handle (and under each scenario, include a few examples as sub-bullets).""",
    }
    plan_messages = [
        explain_system_message,
        explain_user_message,
        explain_assistant_message,
        plan_user_message,
    ]
    if print_text:
        print_messages([plan_user_message])
    plan_response = client.chat.completions.create(
        model=plan_model, messages=plan_messages, temperature=temperature, stream=False
    )
    plan = ""
    if stream:
        for chunk in plan_response:
            delta = chunk.choices[0].delta
            if print_text:
                print_message_delta(delta)
            if "content" in delta:
                plan += delta["content"]
    else:
        plan = plan_response.choices[0].message.content
        if print_text:
            print_message_assistant(plan)
    plan_assistant_message = {"role": "assistant", "content": plan}

    num_bullets = max(plan.count("\n-"), plan.count("\n*"))
    elaboration_needed = num_bullets < approx_min_cases_to_cover
    if elaboration_needed:
        elaboration_user_message = {
            "role": "user",
            "content": f"""In addition to those scenarios above, list a maximum of {num_bullets-approx_min_cases_to_cover} rare or unexpected edge cases (and as before, under each edge case, include a few examples as sub-bullets).""",
        }
        elaboration_messages = [
            explain_system_message,
            explain_user_message,
            explain_assistant_message,
            plan_user_message,
            plan_assistant_message,
            elaboration_user_message,
        ]
        if print_text:
            print_messages([elaboration_user_message])
        elaboration_response = client.chat.completions.create(
            model=plan_model,
            messages=elaboration_messages,
            temperature=temperature,
            stream=False,
        )
        elaboration = ""
        if stream:
            for chunk in elaboration_response:
                delta = chunk.choices[0].delta
                if print_text:
                    print_message_delta(delta)
                if "content" in delta:
                    elaboration += delta["content"]
        else:
            elaboration = elaboration_response.choices[0].message.content
            if print_text:
                print_message_assistant(elaboration)
        elaboration_assistant_message = {"role": "assistant", "content": elaboration}

    # Step 3: Generate the unit test
    package_comment = ""
    if unit_test_package == "pytest":
        package_comment = "# below, each test case is represented by a tuple passed to the @pytest.mark.parametrize decorator"
    execute_system_message = {
        "role": "system",
        "content": "You are a world-class Python developer with an eagle eye for unintended bugs and edge cases. You write careful, accurate unit tests. When asked to reply only with code, you write all of your code in a single block.",
    }
    execute_user_message = {
        "role": "user",
        "content": f"""Using Python and the `{unit_test_package}` package, write a suite of unit tests for the function, following the cases above. Include helpful comments to explain each line. Reply only with code, formatted as follows:

                    ```python
                    # imports
                    import {unit_test_package}  # used for our unit tests
                    {{insert other imports as needed}}

                    # function to test
                    from src.{function_filename.split('/')[-1].replace('.py', '')} import {function_to_test.split('(')[0].strip()}

                    # unit tests
                    {package_comment}
                    {{insert unit test code here}}
                    ```
                    The imports and functions to test part has to be exactly like that!
                    """,
    }
    execute_messages = [
        execute_system_message,
        explain_user_message,
        explain_assistant_message,
        plan_user_message,
        plan_assistant_message,
    ]
    if elaboration_needed:
        execute_messages += [elaboration_user_message, elaboration_assistant_message]
    execute_messages += [execute_user_message]
    if print_text:
        print_messages([execute_system_message, execute_user_message])

    logging.info("Running unit test generation.")
    execute_response = client.chat.completions.create(
        model=execute_model,
        messages=execute_messages,
        temperature=temperature,
        stream=False,
    )
    execution = ""
    if stream:
        for chunk in execute_response:
            delta = chunk.choices[0].delta
            if print_text:
                print_message_delta(delta)
            if "content" in delta:
                execution += delta["content"]
    else:
        execution = execute_response.choices[0].message.content
        if print_text:
            print_message_assistant(execution)

    code = execution.split("```python")[1].split("```")[0].strip()
    try:
        ast.parse(code)
    except SyntaxError as e:
        print(f"Syntax error in generated code: {e}")
        if reruns_if_fail > 0:
            print("Rerunning...")
            return unittest_flow(
                function_to_test=function_to_test,
                function_filename=function_filename,
                unit_test_package=unit_test_package,
                approx_min_cases_to_cover=approx_min_cases_to_cover,
                print_text=print_text,
                explain_model=explain_model,
                plan_model=plan_model,
                execute_model=execute_model,
                temperature=temperature,
                reruns_if_fail=reruns_if_fail
                - 1,  # decrement rerun counter when calling again
            )

    # Write the unit test to a file
    output_dir = os.path.join(os.getcwd(), "tests/unit")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "test_functions.py")

    with open(output_file, "w") as f:
        f.write(code)

    logging.info(f"Unit tests written to {output_file}")

    return output_file


def run_pytest(test_file):
    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    sys.stdout.write(result.stdout)
    # sys.stderr.write(result.stderr)
    return result.returncode, result.stdout


def correct_function(
    function_to_test,
    function_filename,
    test_results,
    failed_test_cases,
    explain_model="gpt-3.5-turbo",
    temperature=0.6,
):
    """
    Corrects a Python function based on unit test failures provided as inputs.

    Parameters
    ----------
    function_to_test : str
        The name of the function to be corrected.
    function_filename : str
        The filename where the unit tests for the function are located.
    test_results : str
        String detailing the results of running the unit tests.
    failed_test_cases : str
        Detailed descriptions of which test cases failed and possibly why.
    explain_model : str, optional
        The name of the AI model used to generate corrections (default is "gpt-3.5-turbo").
    temperature : float, optional
        The creativity temperature for generating the correction (default is 0.4).

    Returns
    -------
    tuple
        A tuple containing the corrected function as a string and the path to the file where the corrected function is written.

    Raises
    ------
    IndexError
        If extracting the corrected function from the AI's response fails.

    Examples
    --------
    >>> corrected_func, path = correct_function(
            'my_func', 'test_my_func.py', 'Tests passed: 0, Tests failed: 1',
            'Failed at input 3: expected 9, got 3', 'gpt-3.5-turbo', 0.4
        )
    """
    client = OpenAI()
    logging.info("Starting function correction...")

    correction_system_message = {
        "role": "system",
        "content": f"""
        Correction of Python Function Based on Unit Tests

        Description:
        You are provided with a Python unittest file named {function_filename} which includes several unit tests for a function called {function_to_test}. Your task is to create or modify the Python function {function_to_test} such that it passes all the provided unit tests. The unittest file includes various test cases with expected outputs that {function_to_test} needs to meet.

        Input:

        File Name: {function_filename} - This file contains all the unit tests for the function {function_to_test}.
        Test Details: Describe each test case briefly, including inputs and the expected outputs.
        Task:

        Analyze the unit tests to understand the requirements and behaviors expected from {function_to_test}.
        Write or revise the Python code for {function_to_test} to ensure it satisfies all the conditions set by the tests in {function_filename}.
        Output:

        Python code for {function_to_test} that successfully passes all the tests in the provided unittest file.
        Additional Instructions:

        Ensure the code is clean, well-commented, and adheres to standard Python conventions.
        Provide any assumptions made during the code correction process.
        If any test case is ambiguous or seems incorrect, note your observations and how you addressed them.
        """,
    }

    correction_user_message = {
        "role": "user",
        "content": f"""Please correct the following Python function to make it pass the given unit tests. The following are the test results and error messages:

Test results:
{test_results}

Failed test cases:
{failed_test_cases}

Ensure the corrected function maintains its intended functionality and fixes any bugs.

```python
{function_to_test}
```""",
    }

    correction_messages = [correction_system_message, correction_user_message]
    correction_response = client.chat.completions.create(
        model=explain_model,
        messages=correction_messages,
        temperature=temperature,
        stream=False,
    )
    corrected_function_content = correction_response.choices[0].message.content

    try:
        corrected_function = (
            corrected_function_content.split("```python")[1].split("```")[0].strip()
        )
    except IndexError:
        logging.error("Failed to extract corrected function from response.")
        corrected_function = (
            function_to_test  # Fallback to the original function in case of error
        )

    output_dir = os.path.join(os.getcwd(), "src")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, function_filename)

    with open(output_file, "w") as f:
        f.write(corrected_function)

    return corrected_function, output_file


def extract_failed_test_cases(test_output):
    try:
        # Pattern to match the failed test cases
        failed_cases_pattern = r"________________ (.*?) __________________"
        failed_cases = re.findall(failed_cases_pattern, test_output)

        # Pattern to match the error messages associated with the failed test cases
        error_messages_pattern = r"E\s+(.*?)\n"
        error_messages = re.findall(error_messages_pattern, test_output, re.DOTALL)

        # Combine the failed cases with their respective error messages
        failed_cases_with_errors = [
            f"Test case: {case}\nError: {error}"
            for case, error in zip(failed_cases, error_messages)
        ]

        return failed_cases_with_errors
    except Exception as e:
        logging.error(f"Error extracting failed test cases: {e}")
        return []
