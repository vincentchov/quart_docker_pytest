# src/quart_docker_pytest/api/__init__.py
"""Quart Docker Pytest API."""
import asyncio

from quart import Quart

from quart_docker_pytest.models.background_service import BackgroundService
from quart_docker_pytest.services.users import Users


users_service = Users()
_background_tasks: list[tuple[BackgroundService, asyncio.Task[None]]] = []


async def start_background_services() -> None:
    """Starts Quart app background services.

    Runs background services and makes them available later to cancel
    on-app-shutdown.
    """
    loop = asyncio.get_event_loop()
    _background_tasks.append(
        (users_service, loop.create_task(users_service.task_start()))
    )


async def stop_background_services() -> None:
    """Stops Quart app background services.

    Cancels each background service, allowing them to do some cleanup
    logic beforehand.
    """
    for service, task in _background_tasks:
        await service.on_task_cancel(task)


def create_app() -> Quart:
    """Main entrypoint for the Quart app/API.

    Registers blueprints, startup/shutdown logic, and returns
    an instance of the app, but does not actually run the app.
    """
    app = Quart(__name__)

    from quart_docker_pytest.api.users.views import users_blueprint

    app.register_blueprint(users_blueprint)

    app.before_serving(start_background_services)
    app.after_serving(stop_background_services)

    return app
