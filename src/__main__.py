# src/__main__.py

import sys

# from src.unittest_flow import unittest_flow  # Import your main module or function
from src.unittest_flow2 import (
    unittest_flow,
    run_pytest,
    correct_function,
)  # Import your main module or function

import os

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

    # # Your logic here
    print(f"user_input: {user_input}")
    # print(f"underlying_repo: {underlying_repo}")

    function_to_test, function_filename = read_pig_latin()
    # Generate the tests
    test_file = unittest_flow(
        function_to_test,
        function_filename,
        approx_min_cases_to_cover=10,
        print_text=True,
    )

    # Run the tests
    test_result = run_pytest(test_file)

    # # If tests fail, correct the function and re-run tests
    # idx = 10
    # while test_result > 0 and idx > 0:
    #     corrected_function, corrected_function_file = correct_function(
    #         function_to_test, function_filename
    #     )
    #     print(f"Corrected function:\n{corrected_function}")
    #     # Optionally, re-run the whole process with the corrected function
    #     test_file = unittest_flow(
    #         corrected_function,
    #         function_filename,  # Ensure the filename is passed
    #         approx_min_cases_to_cover=10,
    #         print_text=True,
    #     )
    #     test_result = run_pytest(test_file)
    #     idx -= 1


if __name__ == "__main__":
    main()
