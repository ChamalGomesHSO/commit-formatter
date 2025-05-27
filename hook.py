#!/usr/bin/env python3
import sys
import os

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

DEFAULT_TYPES = [
    ("feat", "A new feature"),
    ("bug", "A bug fix"),
    ("perf", "Improve performance"),
    ("docs", "Documentation-only changes"),
    ("style", "Code style changes (formatting, etc)"),
    ("ref", "Code refactor without behavior change"),
    ("ci", "CI/CD configuration or scripts"),
]

def load_config():
    config_path = ".commit-hook.toml"
    if os.path.exists(config_path):
        with open(config_path, "rb") as f:
            data = tomllib.load(f)
            return data.get("tool", {}).get("commit_hook", {})
    return {}

def main():
    if len(sys.argv) < 2:
        print("No commit message file provided.")
        sys.exit(1)

    commit_msg_file = sys.argv[1]
    config = load_config()
    types = config.get("types", DEFAULT_TYPES)

    print("Select the type of change you are committing:")
    for idx, entry in enumerate(types, start=1):
        value = entry["value"] if isinstance(entry, dict) else entry[0]
        name = entry["name"] if isinstance(entry, dict) else entry[1]
        print(f"{idx}. {value}: {name}")

    while True:
        try:
            choice = int(input("Enter number (1-{}): ".format(len(types))))
            if 1 <= choice <= len(types):
                break
        except ValueError:
            pass
        print("Invalid selection. Try again.")

    change_type = types[choice - 1]["value"] if isinstance(types[choice - 1], dict) else types[choice - 1][0]
    message = input("Write a short and imperative summary of the code changes:\n> ").strip()

    final_message = f"{change_type}: {message}"
    with open(commit_msg_file, 'w') as f:
        f.write(final_message + "\n")

if __name__ == "__main__":
    main()
