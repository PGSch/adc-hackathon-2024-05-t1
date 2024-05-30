import ast
import os
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
    temperature: float = 0.4,
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
        print_message_assistant(plan)
    plan_assistant_message = {"role": "assistant", "content": plan}

    num_bullets = max(plan.count("\n-"), plan.count("\n*"))
    elaboration_needed = num_bullets < approx_min_cases_to_cover
    if elaboration_needed:
        elaboration_user_message = {
            "role": "user",
            "content": f"""In addition to those scenarios above, list a few rare or unexpected edge cases (and as before, under each edge case, include a few examples as sub-bullets).""",
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
                    The imports and functions to test part has to be exactly like that.
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

    print(f"Unit tests written to {output_file}")

    return output_file


def run_pytest(test_file):
    result = subprocess.run(["pytest", test_file], capture_output=True, text=True)
    print(result.stdout)
    return result.returncode


def correct_function(
    function_to_test, function_filename, explain_model="gpt-3.5-turbo", temperature=0.4
):
    client = OpenAI()
    correction_system_message = {
        "role": "system",
        "content": "You are a world-class Python developer with an eagle eye for unintended bugs and edge cases. You carefully correct code with great detail and accuracy.",
    }
    correction_user_message = {
        "role": "user",
        "content": f"""Please correct the following Python function to make it pass the given unit tests. Ensure the corrected function maintains its intended functionality and fixes any bugs.

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
    corrected_function = (
        correction_response.choices[0]
        .message.content.split("```python")[1]
        .split("```")[0]
        .strip()
    )

    # Write the corrected function to a file
    output_dir = os.path.join(os.getcwd(), "src")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, function_filename)

    with open(output_file, "w") as f:
        f.write(corrected_function)

    print(f"Corrected function written to {output_file}")

    return corrected_function, output_file
