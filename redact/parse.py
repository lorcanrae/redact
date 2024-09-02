import os
import re
import click


def process_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    output_lines = []
    inside_solution_block = False

    for line in lines:
        if "<!-- $SOLUTION_START -->" in line:
            inside_solution_block = True
            continue
        elif "<!-- $SOLUTION_END -->" in line:
            inside_solution_block = False
            continue

        if not inside_solution_block:
            output_lines.append(line)

    output_content = "".join(output_lines)
    return output_content


def normalise_newlines(content):
    return re.sub(r'\n{3,}', '\n\n', content)


@click.command()
@click.argument(
    "source_dir", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
def solution(source_dir):
    """Process markdown files in the given directory and create README.md files."""
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file == 'SOLUTION.md':
                source_file_path = os.path.join(root, file)
                readme_content = process_markdown_file(source_file_path)
                readme_content = normalise_newlines(readme_content)
                readme_path = os.path.join(root, "README.md")

                with open(readme_path, "w", encoding="utf-8") as readme_file:
                    readme_file.write(readme_content)

                click.echo(f"Created README.md at: {readme_path}")


if __name__ == "__main__":

    import sys

    source_dir = sys.argv[1]
    solution(source_dir)
