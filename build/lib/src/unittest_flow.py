import sys
import os
import importlib
import subprocess
import logging
from openai import OpenAI
import src.unittest_python as ut
import pytest

# Setup logger
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[logging.StreamHandler(sys.stdout)])
logger = logging.getLogger(__name__)

def unittest_flow(user_input, underlying_repo):
    # Ensure stream is defined at the start of the function
    stream = False
    logger.debug(f"stream initialized to: {stream}")

    # Get the directory of the current file (unittest_flow.py)
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    logger.debug(f"current_file_dir: {current_file_dir}")

    # Construct the absolute path to the requirements.txt
    requirements_path = os.path.join(current_file_dir, "..", "requirements.txt")
    logger.debug(f"requirements_path: {requirements_path}")

    with open(requirements_path, "r") as file:
        package_names = [line.strip() for line in file]

        # Import the packages dynamically
        for package_name in package_names:
            try:
                importlib.import_module(package_name)
            except ImportError:
                logger.warning(f"Failed to import '{package_name}'. Attempting to install...")
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", package_name]
                )
                try:
                    importlib.import_module(package_name)
                    logger.info(f"Successfully installed and imported '{package_name}'")
                except ImportError:
                    logger.error(f"Failed to install '{package_name}'. Please install it manually.")

    # Add the path to the 'src' directory
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))

    def setup_environment():
        logger.debug("Setting up environment")
        # Print the environment variable to confirm it's set
        logger.debug(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")

    # Call the function
    setup_environment()

    # Get the directory of the current file (unittest_flow.py)
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    logger.debug(f"current_file_dir: {current_file_dir}")

    # Construct the absolute path to the pig_latin.py
    pig_latin_path = os.path.join(current_file_dir, ".", "pig_latin.py")
    logger.debug(f"pig_latin_path: {pig_latin_path}")

    # Read the contents of pig_latin.py
    with open(pig_latin_path, "r") as file:
        function_to_test = file.read()

    logger.debug(f"function_to_test: {function_to_test}")

    unit_test_package: str = "pytest"
    approx_min_cases_to_cover: int = 10
    print_text: bool = True
    explain_model: str = "gpt-3.5-turbo"
    plan_model: str = "gpt-3.5-turbo"
    execute_model: str = "gpt-3.5-turbo"
    temperature: float = 0.4
    reruns_if_fail: int = 1
    function_to_test = function_to_test

    client = OpenAI()
    # Step 1: Generate an explanation of the function

    # create a markdown-formatted message that asks GPT to explain the function, formatted as a bullet list
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
        ut.print_messages(explain_messages)

    logger.debug("Before calling the OpenAI API")
    explanation_response = client.chat.completions.create(
        model=explain_model,
        messages=explain_messages,
        temperature=temperature,
        stream=stream,
    )
    logger.debug("explanation_response FINISHED")
    explanation = ""
    logger.debug(f"Stream value before check: {stream}")
    if stream:
        logger.debug("Streaming response")
        for chunk in explanation_response:
            delta = chunk.choices[0].delta
            if print_text:
                ut.print_message_delta(delta)
            if "content" in delta:
                explanation += delta["content"]
        explain_assistant_message = {"role": "assistant", "content": explanation}
    else:
        logger.debug("Non-streaming response")
        explanation = explanation_response.choices[0].message.content

    return explanation_response.choices[0].message.content
