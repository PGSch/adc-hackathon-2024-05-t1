import argparse
import logging
import os
from src.unittest_flow import UnitTestFlow


def configure_logging():
    """Configures the basic logging setup."""
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def get_openai_models():
    """Retrieve OpenAI model settings from environment variables or use defaults."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("The OpenAI API key must be set in the environment.")

    # Set the model names based on environment configuration or defaults
    overall_model = os.getenv("OVERALL_MODEL", "gpt-3.5-turbo")
    return overall_model, overall_model, overall_model


def main():
    configure_logging()
    explain_model, plan_model, execute_model = get_openai_models()

    parser = argparse.ArgumentParser(
        description="Generate and correct unit tests for a specified function."
    )
    parser.add_argument(
        "--file_name",
        type=str,
        required=True,
        help="The file name containing the target function or class.",
    )
    parser.add_argument(
        "--class_or_method",
        type=str,
        required=True,
        help="The name of the class or method to test.",
    )

    args = parser.parse_args()
    logging.info(f"file_name: {args.file_name}")
    logging.info(f"class_or_method: {args.class_or_method}")
    logging.info("Starting test generation and correction loop...")
    # Instance of the UnitTestFlow class
    test_flow = UnitTestFlow(
        function_to_test=args.class_or_method,
        function_filename=args.file_name,
        explain_model=explain_model,
        plan_model=plan_model,
        execute_model=execute_model,
        approx_min_cases_to_cover=10,
        reruns_if_fail=5,
    )

    # Generate the tests and potentially run correction loops
    test_file_path = test_flow.run()

    previous_failed_cases = None
    failed_cases_unchanged = 0
    max_attempts = 3

    while failed_cases_unchanged < max_attempts:
        pytest_result = test_flow.run_pytest(test_file_path)
        logging.info("__main__/while/pytest_result:")
        # print(pytest_result)
        if pytest_result.returncode == 0:
            logging.info("All tests passed successfully!")
            break

        # failed_cases = test_flow.extract_failed_test_cases(pytest_result)
        failed_cases = pytest_result.stdout
        if failed_cases == previous_failed_cases:
            failed_cases_unchanged += 1
            logging.warning(
                f"Try {failed_cases_unchanged} - No change in failed test cases after correction. Reviewing test feasibility..."
            )

        if failed_cases_unchanged >= max_attempts:
            logging.error("Maximum attempts reached with no resolution.")
            logging.info("Regenerating or analyzing tests due to repeated failures.")
            failed_cases_unchanged = 0
            # Instance of the UnitTestFlow class
            test_flow = UnitTestFlow(
                function_to_test=args.class_or_method,
                function_filename=args.file_name,
                explain_model=explain_model,
                plan_model=plan_model,
                execute_model=execute_model,
                temperature=0.4 + 0.6 * failed_cases_unchanged / max_attempts,
            )
            test_file_path = test_flow.run()
            continue

        previous_failed_cases = failed_cases

        # Assuming we have a method to handle test corrections:
        # This part should be adjusted according to your real correction mechanism
        # For now, re-running the test generation as a placeholder for actual correction logic
        test_file_path = test_flow.run()

    logging.info("Test generation and correction loop completed.")


if __name__ == "__main__":
    main()
