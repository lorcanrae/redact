import os
import click

from redact.errors import MarkdownParsingError
from redact.markdown_helpers import (
    get_file_content,
    get_indentation_level,
    normalise_newlines,
)


def process_markdown_file(lines, file_path=None) -> str:

    output_lines = []
    inside_solution_block = False
    tag_start_count = 0
    tag_end_count = 0

    for i, line in enumerate(lines):
        ### $SOLUTION_START handling
        if "<!-- $SOLUTION_START -->" in line:
            ### Start ordering check
            if inside_solution_block:
                raise MarkdownParsingError(
                    f"Error in file `{file_path}`, at line {i + 1}: Encountered `<!-- $SOLUTION_START -->` without closing the previous block with `<!-- $SOLUTION_END -->`."
                )

            ### Start indent check
            if i + 1 < len(lines):
                current_indent = get_indentation_level(line)
                next_line_indent = get_indentation_level(lines[i + 1])
                if current_indent != next_line_indent:
                    raise MarkdownParsingError(
                        f"Error in file `{file_path}`, at line {i + 2}: Indentation mismatch after `<-- $SOLUTION_START -->`.\n"
                        f"Expected {current_indent} spaces but found {next_line_indent}."
                    )

            tag_start_indent = current_indent

            inside_solution_block = True
            tag_start_count += 1

            continue

        ### $SOLUTION_END handling
        elif "<!-- $SOLUTION_END -->" in line:
            ### End ordering check
            if not inside_solution_block:
                raise MarkdownParsingError(
                    f"Error in file `{file_path}`, at line {i + 1}: Encountered `<!-- $SOLUTION_END -->` without closing the previous block with `<!-- $SOLUTION_START -->`."
                )

            ### End indent check - end indent == start indent
            if i > 0:
                current_indent = get_indentation_level(line)
                if current_indent != tag_start_indent:
                    raise MarkdownParsingError(
                        f"Error in file `{file_path}`, at line {i + 1}: Indentation mismatch before `<-- $SOLUTION_END -->`.\n"
                        f"Expected {tag_start_indent} spaces but found {current_indent}."
                    )

            inside_solution_block = False
            tag_end_count += 1

            continue

        if not inside_solution_block:
            output_lines.append(line)

    # Unbalanced tag check
    if tag_start_count != tag_end_count:
        raise MarkdownParsingError(
            f"Error in file `{file_path}`: Unbalanced `<!-- $SOLUTION_START -->` and `<!-- $SOLUTION_END -->` tags."
        )

    output_content = "".join(output_lines)
    return output_content


def process_single_file(file_path) -> None:
    """
    Process a single SOLUTION.md file.
    """
    if not file_path.endswith("SOLUTION.md"):
        click.echo(f"Skipping non-SOLUTION.md file: {file_path}")
        return

    try:
        # Process
        readme_content = get_file_content(file_path)
        readme_content = process_markdown_file(readme_content, file_path)
        readme_content = normalise_newlines(readme_content)

        readme_path = os.path.join(os.path.dirname(file_path), "README.md")

        with open(readme_path, "w", encoding="utf-8") as readme_file:
            readme_file.write(readme_content)

        click.echo(f"Created README.md at: {readme_path}")

    except MarkdownParsingError as e:
        click.echo(f"Markdown parsing error: {e}")
        return


def process_directory(directory_path) -> None:
    """
    Process all SOLUTION.md files in a directory.
    """
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file == "SOLUTION.md":
                process_single_file(os.path.join(root, file))


@click.command()
@click.argument("source", type=click.Path(exists=True))
def solution(source) -> None:
    """
    Process either a single SOLUTION.md or all SOLUTION.md files in a directory
    """
    if os.path.isfile(source):
        process_single_file(source)

    elif os.path.isdir(source):
        process_directory(source)

    else:
        click.echo("Invalid source. Please provide a valid file or directory.")


if __name__ == "__main__":

    # Don't need to use sys.argv - click handles input
    solution()
