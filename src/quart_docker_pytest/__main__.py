"""Command-line interface."""
import click

from quart_docker_pytest.utils import caddy


@click.group()
@click.version_option()
def main() -> None:
    """Main command group for Quart Docker Pytest management CLI."""


@main.command()
def init_secrets_and_caddy() -> None:
    """Initialization logic needed for other Docker services to work.

    Templates a Caddyfile for the reverse proxy to be able to start.
    """
    caddy.init_caddy()


if __name__ == "__main__":
    main(prog_name="quart-docker-pytest")  # pragma: no cover
