# src/__main__.py

from src.unittest_flow import (
    unittest_flow,
    run_pytest,
    correct_function,
    extract_failed_test_cases,
)

import sys
import logging
import os
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO)


openai_api_key = os.getenv("OPENAI_API_KEY")
# overall_model = "gpt-4o"
overall_model = False
if overall_model:
    explain_model = overall_model
    plan_model = overall_model
    execute_model = overall_model
else:
    explain_model = "gpt-3.5-turbo"
    plan_model = "gpt-3.5-turbo"
    execute_model = "gpt-3.5-turbo"
if openai_api_key is None:
    raise ValueError("The OpenAI API key must be set in the environment.")


def read_function(function_file: str):
    """

    Args:
        function_file (str): e.g. 'pig_latin.py'

    Returns:
        _type_: _description_
    """
    # Get the directory of the current file (unittest_flow.py)
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the pig_latin.py
    function_path = os.path.join(current_file_dir, ".", function_file)

    # Read the contents of pig_latin.py
    with open(function_path, "r") as file:
        function_to_test = file.read()

    return function_to_test, function_path


def print_test_file():
    output_file = os.path.join(os.getcwd(), "tests/unit/test_functions.py")

    if not os.path.exists(output_file):
        print(f"The file {output_file} does not exist.")
        return

    with open(output_file, "r") as f:
        content = f.read()

    print(f"Contents of {output_file}:\n")
    print(content)


def main():
    parser = argparse.ArgumentParser(description="Description of your script")
    parser.add_argument("--user_input", type=str, required=True, help="User input")
    parser.add_argument(
        "--underlying_repo", type=str, required=True, help="Underlying repository"
    )

    args = parser.parse_args()
    user_input = args.user_input
    underlying_repo = args.underlying_repo

    print(f"user_input: {user_input}")
    print(f"underlying_repo: {underlying_repo}")

    function_to_test, function_filename = read_function("inventory_manager.py")
    logging.info("Starting test generation and correction loop...")
    previous_failed_cases = None
    failed_cases_changed = 0
    # Generate the tests with 100% code coverage
    test_file = unittest_flow(
        function_to_test,
        function_filename,
        approx_min_cases_to_cover=10,
        reruns_if_fail=5,
        print_text=False,
        explain_model=explain_model,
        plan_model=plan_model,
        execute_model=execute_model,
    )

    # for _ in range(0, 3):
    idx = 3
    ref_idx = idx
    while idx > 0:
        # Run the tests
        test_result, test_output = run_pytest(test_file)
        failed_test_cases = extract_failed_test_cases(test_output)

        if test_result == 0:
            logging.info("All tests passed successfully.")
            break

        if previous_failed_cases == failed_test_cases:
            failed_cases_changed += 1
            logging.warning(
                f"Try {failed_cases_changed} - No change in failed test cases after correction. Reviewing test feasibility..."
            )
            # Additional logic to handle unchanged tests or regenerate tests

        if failed_cases_changed > 5:
            logging.info("Regenerating or analyzing tests due to repeated failures.")
            # Generate the tests again and hope for new better tests
            test_file = unittest_flow(
                corrected_function,
                function_filename,  # Ensure the filename is passed
                approx_min_cases_to_cover=10,
                print_text=False,
                explain_model=explain_model,
                plan_model=plan_model,
                execute_model=execute_model,
                temperature=0.4 + 0.1 * failed_cases_changed,
            )
            idx = ref_idx
            failed_cases_changed = 0
            continue

        logging.info("Different failed cases after correction - try to correct again.")
        # Correct the function based on the test results
        corrected_function, _ = correct_function(
            function_to_test,
            function_filename,
            test_output,
            failed_test_cases,
            explain_model=explain_model,
            temperature=0.4 + 0.1 * failed_cases_changed,
        )
        logging.debug(f"Corrected function:\n{corrected_function}")

        function_to_test = corrected_function  # Update the function to test with the corrected function
        previous_failed_cases = failed_test_cases  # Update the record of failed cases

    logging.info("Test generation and correction loop completed.")


if __name__ == "__main__":
    main()
