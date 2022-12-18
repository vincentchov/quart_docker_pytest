"""Background Service."""

import asyncio
from typing import Protocol


class BackgroundService(Protocol):
    """BackgroundService Protocol.

    All classes inheriting from this should implement these methods to be
    considered a background service.
    """

    async def task_start(self) -> None:
        """Performs initial set-up, then runs the background service."""
        ...

    @classmethod
    async def on_task_cancel(cls, task: asyncio.Task[None]) -> None:
        """Allows the service to do some clean-up before gracefully stopping."""
        ...
