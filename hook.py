#!/usr/bin/env python3
import sys
import os

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

DEFAULT_TYPES = [
    {"value": "feat", "name": "A new feature"},
    {"value": "bug", "name": "A bug fix"},
    {"value": "perf", "name": "Improve performance"},
    {"value": "docs", "name": "Documentation-only changes"},
    {"value": "style", "name": "Code style changes (formatting, etc)"},
    {"value": "ref", "name": "Code refactor without behavior change"},
    {"value": "ci", "name": "CI/CD configuration or scripts"},
]

def load_config():
    config_path = ".commit-hook.toml"
    if os.path.exists(config_path):
        with open(config_path, "rb") as f:
            try:
                config = tomllib.load(f)
                return config.get("tool", {}).get("commit_hook", {})
            except tomllib.TOMLDecodeError as e:
                print(f"Error parsing {config_path}: {e}")
    return {}

def is_commit_message_present(path):
    """Return True if commit message already exists and looks valid"""
    try:
        with open(path, "r") as f:
            contents = f.read().strip()
            return bool(contents)
    except Exception:
        return False

def prompt_choice(types):
    print("Select the type of change you are committing:")
    for idx, entry in enumerate(types, start=1):
        print(f"{idx}. {entry['value']}: {entry['name']}")

    while True:
        try:
            choice = int(input(f"Enter number (1-{len(types)}): ").strip())
            if 1 <= choice <= len(types):
                return types[choice - 1]["value"]
        except ValueError:
            pass
        print("Invalid selection. Please enter a number.")

def prompt_message():
    return input("Write a short and imperative summary of the code changes:\n> ").strip()

def main(commit_msg_file):
    if is_commit_message_present(commit_msg_file):
        return  # Message already exists (e.g., via -m or merge)

    config = load_config()
    types = config.get("types", DEFAULT_TYPES)

    change_type = prompt_choice(types)
    message = prompt_message()

    final_message = f"{change_type}: {message}"
    with open(commit_msg_file, "w") as f:
        f.write(final_message + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: hook.py <path_to_commit_msg_file>")
        sys.exit(1)
    main(sys.argv[1])
