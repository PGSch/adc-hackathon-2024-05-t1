    previous_failed_cases = None
    failed_cases_changed = 0
    failed_cases_changed_max = 3

    idx = 3
    ref_idx = idx
    while idx > 0:
        # Run the tests
        test_output = run_pytest(test_file)

        if test_output["returncode"] == 0:
            logging.info("All tests passed successfully!")
            break

        failed_test_cases = extract_failed_test_cases(test_output)

        if previous_failed_cases == failed_test_cases:
            failed_cases_changed += 1
            logging.warning(
                f"Try {failed_cases_changed} - No change in failed test cases after correction. Reviewing test feasibility..."
            )
            # Additional logic to handle unchanged tests or regenerate tests

        if failed_cases_changed == failed_cases_changed_max:
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
                temperature=0.4 + 0.6 * failed_cases_changed / failed_cases_changed_max,
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