import re


def get_file_content(file_path) -> list:
    """Return the contents of a markdown file as a list"""
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()
    return lines


def get_indentation_level(line: str) -> int:
    """Return the number of leading spaces in a line"""
    return len(line) - len(line.lstrip())


def normalise_newlines(content: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", content)


if __name__ == "__main__":
    content = get_file_content("tests/data/a_new_challenge/SOLUTION.md")
    print(content)
