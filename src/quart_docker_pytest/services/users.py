"""Users Service."""
import asyncio
import json
from contextlib import suppress

import httpx

from quart_docker_pytest.models.background_service import BackgroundService
from quart_docker_pytest.models.user import User


class Users(BackgroundService):
    """Users Service.

    Used for polling for users.
    """

    users: list[User] = []

    async def fetch_users(self) -> None:
        """Fetches users and updates the list of users."""
        async with httpx.AsyncClient(
            base_url="https://jsonplaceholder.typicode.com"
        ) as client:
            try:
                r = await client.get("/users")
                data = json.loads(r.text)
                self.users = [User.from_dict(d) for d in data]
            except Exception as e:
                print(e)

    async def poll_for_users(self) -> None:
        """Does the actual polling."""
        await self.fetch_users()
        await asyncio.sleep(10)

    def data(self) -> list[User]:
        """Return all users that have been fetched."""
        return self.users

    async def task_start(self) -> None:
        """Initializes list of users, and then polls in the background."""
        await self.fetch_users()
        while True:
            await self.fetch_users()
            await asyncio.sleep(30)

    @classmethod
    async def on_task_cancel(cls, task: asyncio.Task[None]) -> None:
        """Allows the background service to be stopped gracefully."""
        with suppress(asyncio.CancelledError):
            task.cancel()
