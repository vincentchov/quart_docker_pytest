# src/quart_docker_pytest/api/auth/views.py
"""API-side Auth Service Views."""
from quart import Blueprint
from quart import Response
from quart import jsonify
from quart import request

from quart_docker_pytest.api import users_service


users_blueprint = Blueprint("users", __name__, url_prefix="/users")


@users_blueprint.route("/", methods=["GET", "POST"])
async def index() -> Response:
    """Users Blueprint index.

    Returns a "Hello, world" JSON by default, or tries to echo JSON that is
    passed into it.
    """
    default_json = {
        "message": "Hello, world!",
        "someNumber": 1,
    }
    if request.method == "GET":
        return jsonify(default_json)
    else:
        some_json = await request.get_json()
        print(some_json)
        return jsonify(some_json)


@users_blueprint.route("/data/")
async def data() -> Response:
    """Get the entire users record."""
    return jsonify(users_service.data())
