"""Test cases for the Users blueprint."""
import pytest
from quart.typing import TestAppProtocol
from quart.typing import TestClientProtocol

from quart_docker_pytest.models.user import User


@pytest.mark.asyncio
async def test_user_index_returns_default_json(app: TestAppProtocol) -> None:
    """Tests default JSON response."""
    client: TestClientProtocol = app.test_client()
    response = await client.get("/users/")
    assert response.status_code == 200
    body = await response.get_json()
    assert body == {"message": "Hello, world!", "someNumber": 1}


@pytest.mark.asyncio
async def test_user_index_echoes_json(app: TestAppProtocol) -> None:
    """Tests that JSON can be echoed back."""
    test_payload = {"msg": "Meow", "test_boolean": True}
    client: TestClientProtocol = app.test_client()
    response = await client.post("/users/", json=test_payload)
    assert response.status_code == 200
    body = await response.get_json()
    assert body == test_payload


@pytest.mark.asyncio
async def test_user_data_loads_after_start(app: TestAppProtocol) -> None:
    """Tests that user data is loaded by the Quart app after 10s."""
    client: TestClientProtocol = app.test_client()
    response = await client.get("/users/data/")
    users = await response.get_json()
    assert len(users) > 0
    example_record = User.from_dict(users[0])
    assert example_record.id
    assert example_record.name != ""
