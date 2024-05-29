# src/__main__.py

import sys
from src.unittest_flow import unittest_flow  # Import your main module or function

import os

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key is None:
    raise ValueError("The OpenAI API key must be set in the environment.")


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

    output = unittest_flow(user_input, underlying_repo)

    print(output)


if __name__ == "__main__":
    main()
