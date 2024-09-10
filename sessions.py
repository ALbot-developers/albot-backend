from fastapi import HTTPException
from fastapi_sessions.session_verifier import SessionVerifier
from pydantic import BaseModel

import envs
from uuid import UUID
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters


class SessionData(BaseModel):
    oauth2_state: str


SESSION_VERIFIER = None


def get_verifier():
    global SESSION_VERIFIER
    backend = InMemoryBackend[UUID, SessionData]()
    if not SESSION_VERIFIER:
        SESSION_VERIFIER = BasicVerifier(
            identifier="general_verifier",
            auto_error=True,
            backend=backend,
            auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
        )
    return SESSION_VERIFIER


def get_cookie():
    cookie_params = CookieParameters()
    # Uses UUID
    cookie = SessionCookie(
        cookie_name="cookie",
        identifier="general_verifier",
        auto_error=True,
        secret_key=envs.SESSION_SECRET,
        cookie_params=cookie_params,
    )
    return cookie


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
            self,
            *,
            identifier: str,
            auto_error: bool,
            backend: InMemoryBackend[UUID, SessionData],
            auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        return True
