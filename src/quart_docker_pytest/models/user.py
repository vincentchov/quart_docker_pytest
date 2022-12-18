"""User model."""
from dataclasses import dataclass
from dataclasses import field

from dataclasses_json import DataClassJsonMixin
from dataclasses_json import LetterCase
from dataclasses_json import dataclass_json


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass(frozen=True)
class User(DataClassJsonMixin):
    """User model.

    Represents a User returned from the test API.
    """

    id: int = field()
    name: str = field()
    username: str = field()
    email: str = field()
