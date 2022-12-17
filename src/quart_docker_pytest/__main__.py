"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Quart Docker Pytest."""


if __name__ == "__main__":
    main(prog_name="quart-docker-pytest")  # pragma: no cover
