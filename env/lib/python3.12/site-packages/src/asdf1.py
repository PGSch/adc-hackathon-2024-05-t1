# src/__main__.py

from src.unittest_flow import (
    unittest_flow,
    run_pytest,
    correct_function,
    extract_failed_test_cases,
)  # Import your main module or function

import argparse
import logging
from openai import OpenAI


# Set up logging
logging.basicConfig(level=logging.INFO)


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

    function_to_test, function_filename = (
        "initial_function",
        "test_function.py",
    )  # Example placeholders
    logging.info("Starting test generation and correction loop...")

    previous_failed_cases = None
    tests_changed = True

    for _ in range(0, 3):  # Loop up to three times or until tests pass
        # Run the tests
        test_file = unittest_flow(
            function_to_test,
            function_filename,
            unit_test_package="pytest",
            approx_min_cases_to_cover=7,
            print_text=FALSE,
            explain_model="gpt-3.5-turbo",
            plan_model="gpt-3.5-turbo",
            execute_model="gpt-3.5-turbo",
        )
        test_result, test_output = run_pytest(test_file)
        failed_test_cases = extract_failed_test_cases(test_output)

        if test_result == 0:
            logging.info("All tests passed successfully.")
            break

        if previous_failed_cases == failed_test_cases:
            logging.warning(
                "No change in failed test cases after correction. Reviewing test feasibility..."
            )
            # Additional logic to handle unchanged tests or regenerate tests
            tests_changed = False
            break  # or continue with a modified approach

        # Correct the function based on the test results
        corrected_function, _ = correct_function(
            function_to_test,
            function_filename,
            test_output,
            failed_test_cases,
            explain_model="gpt-3.5-turbo",
        )
        function_to_test = corrected_function  # Update the function to test with the corrected function
        previous_failed_cases = failed_test_cases  # Update the record of failed cases

    if not tests_changed:
        # Logic to regenerate tests or further analyze them
        logging.info("Regenerating or analyzing tests due to repeated failures.")
        # You might want to call `unittest_flow` with different parameters or review the test cases manually

    logging.info("Test generation and correction loop completed.")


if __name__ == "__main__":
    main()
