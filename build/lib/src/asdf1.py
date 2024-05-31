# src/__main__.py

import sys
import logging
import os

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# from src.unittest_flow import unittest_flow  # Import your main module or function
from src.unittest_flow2 import (
    unittest_flow,
    run_pytest,
    correct_function,
    extract_failed_test_cases,
)  # Import your main module or function

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("The OpenAI API key must be set in the environment.")


def read_pig_latin():
    # Get the directory of the current file (unittest_flow.py)
    current_file_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the pig_latin.py
    pig_latin_path = os.path.join(current_file_dir, ".", "pig_latin.py")

    # Read the contents of pig_latin.py
    with open(pig_latin_path, "r") as file:
        function_to_test = file.read()

    return function_to_test, pig_latin_path


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
    import argparse

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

    function_to_test, function_filename = read_pig_latin()
    logging.info("Starting test generation and correction loop...")

    # Generate the tests
    test_file = unittest_flow(
        function_to_test,
        function_filename,
        approx_min_cases_to_cover=10,
        print_text=True,
        explain_model="gpt-4o",
        plan_model="gpt-4o",
        execute_model="gpt-4o",
    )

    # Run the tests
    test_result, test_output = run_pytest(test_file)
    failed_test_cases = extract_failed_test_cases(test_output)

    if test_results != 0:
        # Correct the function based on the test results
        corrected_function, corrected_function_file = correct_function(
            function_to_test,
            function_filename,
            test_output,
            failed_test_cases,
            explain_model="gpt-4o",
        )
        logging.debug(f"Corrected function:\n{corrected_function}")

        # Run the tests again to verify they now pass
        test_file = unittest_flow(
            corrected_function,
            function_filename,  # Ensure the filename is passed
            approx_min_cases_to_cover=10,
            print_text=True,
            explain_model="gpt-4o",
            plan_model="gpt-4o",
            execute_model="gpt-4o",
        )
        test_result, test_output = run_pytest(test_file)

        if test_result == 0:
            logging.info("All tests passed successfully after correction.")
        else:
            logging.warning("Some tests still failed after correction.")
            logging.warning(f"Failed test output:\n{test_output}")
    else:
        logging.info("All tests passed successfully on the first run.")

    logging.info("Test generation and correction loop completed.")


if __name__ == "__main__":
    main()
