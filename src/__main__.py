# src/__main__.py


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

    # Your logic here
    print(f"user_input: {user_input}")
    print(f"underlying_repo: {underlying_repo}")

    return user_input


if __name__ == "__main__":
    main()
