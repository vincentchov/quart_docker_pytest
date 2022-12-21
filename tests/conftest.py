"""Test cases for the Quart app."""
import asyncio

import pytest
import pytest_asyncio
import quart.typing
from quart import Quart
from typeguard.importhook import install_import_hook


@pytest.fixture(scope="session")
def event_loop():
    """Re-define's Pytest's event loop to session scope."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="app", scope="session")
async def test_app_fixture():
    """Quart app fixture.

    Creates a test app, waits for it to finish starting, then
    cleanly shuts it down at the end of the session.
    """
    with install_import_hook(["quart_docker_pytest"]):
        from quart_docker_pytest.api import create_app

    app: Quart = create_app()
    test_app: quart.typing.TestAppProtocol = app.test_app()
    await test_app.startup()
    await asyncio.sleep(10)
    yield test_app
    await test_app.shutdown()
