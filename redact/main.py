import click
from redact.parse import solution


@click.group()
def cli():
    pass


cli.add_command(solution)


if __name__ == "__main__":
    cli()
