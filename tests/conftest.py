"""Test cases for the Quart app."""
import pytest
import quart.typing
from quart import Quart
from quart.typing import TestAppProtocol
from typeguard.importhook import install_import_hook


@pytest.fixture(name="app", scope="session")
def _test_app_fixture() -> TestAppProtocol:
    with install_import_hook(["quart_docker_pytest"]):
        from quart_docker_pytest.api import create_app

    app: Quart = create_app()
    test_app: quart.typing.TestAppProtocol = app.test_app()
    return test_app
