import logging
import os
import re
import subprocess
import sys
from openai import OpenAI
import pytest

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

COLORS = {
    "system": "\033[0m",  # gray
    "user": "\033[0m",  # gray
    "assistant": "\033[92m",  # green
}


import logging
import os
import re
import subprocess
import sys
from openai import OpenAI

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class UnitTestFlow:
    def __init__(
        self,
        function_to_test,
        function_filename,
        explain_model="gpt-3.5-turbo",
        plan_model="gpt-3.5-turbo",
        execute_model="gpt-3.5-turbo",
        temperature=0.3,
        unit_test_package="pytest",
        approx_min_cases_to_cover=7,
        reruns_if_fail=1,
        stream=False,
    ):
        self.function_to_test = function_to_test
        self.function_filename = function_filename
        self.unit_test_package = unit_test_package
        self.approx_min_cases_to_cover = approx_min_cases_to_cover
        self.explain_model = explain_model
        self.plan_model = plan_model
        self.execute_model = execute_model
        self.temperature = temperature
        self.reruns_if_fail = reruns_if_fail
        self.stream = stream
        self.client = OpenAI()
        self.pytest_result = None

    def run(self):
        """Orchestrates the generation, execution, and correction of tests."""
        test_code_path = self.write_tests(
            self.generate_test_code(self.generate_plan(self.generate_explanation()))
        )
        test_result = self.run_pytest(test_code_path)
        if test_result.returncode != 0:
            logging.info("test_result.returncode != 0")
            if test_result.stdout:
                logging.info("'if failed_cases' TRUE")
                self.correct_function()
            else:
                logging.info("'if failed_cases' FALSE")
        else:
            logging.info("test_result.returncode == 0")
        return test_code_path

    def run_pytest(self, test_file):
        """Executes pytest on a specified file and captures the output."""
        try:
            self.pytest_result = subprocess.run(
                ["pytest", test_file], capture_output=True, text=True
            )
            logging.info("pytest run successful")
            # print(self.pytest_result.stdout)
            # sys.stdout.write(pytest_result.stdout)
            return self.pytest_result
        except subprocess.CalledProcessError as e:
            logging.error(f"An error occurred while running pytest: {e}")
            self.pytest_result = {
                "returncode": e.returncode,
                "stdout": "",
                "stderr": str(e),
            }
            return subprocess.CompletedProcess(
                args=e.cmd, returncode=e.returncode, stdout="", stderr=str(e)
            )

    def correct_function(self):
        logging.info("Initiating function correction based on failed test cases...")
        correction_messages = [
            {
                "role": "system",
                "content": f"{self._build_correction_system_message}",
            },
            {
                "role": "user",
                "content": f"{self._build_correction_user_message}",
            },
        ]
        correction_response = self.client.chat.completions.create(
            model=self.execute_model,
            messages=correction_messages,
            temperature=self.temperature,
            stream=False,
        )
        corrected_code = correction_response.choices[0].message.content
        self.update_function_in_file(corrected_code)

    def update_function_in_file(self, function_code):
        try:
            # Split by "```python" and take the second part, then split by "```" and take the first part
            # function_code = function_code.split("```python")[1].split("```")[0].strip()
            function_code = function_code
        except IndexError:
            logging.error("Failed to extract corrected function from response.")
            return  # Add return to prevent attempting to write if the extraction failed
        file_path = os.path.join(os.getcwd(), "src/" + self.function_filename)
        with open(file_path, "w") as file:
            file.write(function_code)
        logging.info(f"Updated function written to {file_path}")

    def generate_explanation(self):
        """Generates a detailed explanation of the function."""
        messages = [
            {"role": "system", "content": self._build_explain_system_message()},
            {"role": "user", "content": self._build_explain_user_message()},
        ]
        response = self.client.chat.completions.create(
            model=self.explain_model,
            messages=messages,
            temperature=self.temperature,
            stream=self.stream,
        )
        return response.choices[0].message.content

    def generate_plan(self, explanation):
        """Generates a testing plan based on the function explanation."""
        messages = [{"role": "user", "content": self._build_plan_user_message()}]
        response = self.client.chat.completions.create(
            model=self.plan_model,
            messages=messages,
            temperature=self.temperature,
            stream=self.stream,
        )
        return response.choices[0].message.content

    def generate_test_code(self, plan):
        """Generates unit test code based on the testing plan."""
        messages = [{"role": "user", "content": self._build_execute_user_message()}]
        response = self.client.chat.completions.create(
            model=self.execute_model,
            messages=messages,
            temperature=self.temperature,
            stream=self.stream,
        )
        return response.choices[0].message.content

    def write_tests(self, code):
        """Writes generated test code to a file."""
        output_file = os.path.join(os.getcwd(), "tests/unit", "test_functions.py")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        code = code.split("```python")[1].split("```")[0].strip()
        with open(output_file, "w") as f:
            f.write(code)
        logging.info(f"Unit tests written to {output_file}")
        return output_file

    def _build_explain_system_message(self):
        return """
        You are a world-class Python developer. Your task is to meticulously dissect the provided Python function:
        - Explain each element of the function in detail.
        - Identify and describe each logical branch and decision point.
        - Suggest potential edge cases.
        """

    def _build_explain_user_message(self):
        return f"""
        Please provide a comprehensive explanation of the Python function `{self.function_to_test}`:
        - Describe what each line of code is doing.
        - Discuss any potential edge cases.
        This is the function to test:
        ```python
        {self.function_to_test}
        ```
        """

    def _build_plan_user_message(self):
        return f"""
        A good unit test suite for the function `{self.function_to_test}` should:
        - Test behavior for a wide range of inputs using features of `{self.unit_test_package}`.
        - Be easy to read and understand, with clean code and descriptive names.
        """

    def _build_execute_user_message(self):
        # Step 3: Generate the unit test
        test_package_comment = ""
        if self.unit_test_package == "pytest":
            test_package_comment = "# below, each test case is represented by a tuple passed to the @pytest.mark.parametrize decorator"

        # Prepare dynamic parts of the user message
        imports_and_function = f"""# imports
        import {self.unit_test_package}  # used for our unit tests

        # function to test
        from src.{self.function_filename.split('/')[-1].replace('.py', '')} import {self.function_to_test.split('(')[0].strip()}
        """
        return f"""Using Python and the `{self.unit_test_package}` package, write a suite of unit tests for the function, following the cases above. Include helpful comments to explain each line. Reply only with code, formatted as follows:

    ```python
    {imports_and_function}
    # unit tests
    {test_package_comment}
    {{insert unit test code here}}

                    ```
                    The imports and functions to test part has to be exactly like that! However, make sure to import all dependencies that you might add in the cases!
                    """

    def _build_correction_system_message(self):
        return f"""
        Correction of Python Function Based on Unit Tests

        Description:
        A Python unittest file named {self.function_filename} contains several unit tests for the function {self.function_to_test}. Your task is to either modify or create {self.function_to_test} to pass all these tests. The modified or new function should preserve or enhance all functionalities of the original function, excluding any identified bugs.

        Input:
        - File Name: {self.function_filename} - Contains unit tests for {self.function_to_test}.
        - Test Details: Each test case is briefly described with inputs and the expected outputs.

        Task:
        1. Analyze the unit tests to fully understand the intended functionalities and required behaviors of {self.function_to_test}.
        2. Modify or create the Python code for {self.function_to_test} ensuring it meets all test conditions in {self.function_filename}.
        3. Maintain or expand upon the original function's capabilities, correcting or excluding only the faulty behaviors.

        Output:
        - Updated Python code for {self.function_to_test} that successfully passes all the tests in the provided unittest file.

        Additional Instructions:
        - Ensure the code is clean, well-commented, and follows standard Python coding conventions.
        - Document any assumptions made during the code correction process.
        - Address any ambiguous or incorrect test cases in your submission, detailing how you approached and resolved these issues.
        - Consider edge cases and additional scenarios that may not be covered by the tests but are relevant to the function’s use cases.
        """

    def _build_correction_user_message(self):
        return f"""Please correct the following Python function to make it pass the given unit tests. The following are the test results and error messages:
        
        Test results:
        {self.pytest_result}

        Ensure the corrected function maintains its intended functionality and fixes any bugs.

        ```python
        {self.function_to_test}
        ```"""
