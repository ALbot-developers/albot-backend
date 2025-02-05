from dataclasses import dataclass
from typing import Literal


@dataclass
class AuthenticationResponse:
    auth_type: Literal["bearer", "session"]
    message: str
    payload: dict | None = None
