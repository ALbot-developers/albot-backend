from dataclasses import dataclass
from typing import Literal

import aiohttp
from fastapi import Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.constants import BEARER_TOKEN, TURNSTILE_SECRET_KEY
from app.core.error import CustomHTTPException
from app.services.user import get_guild


# Bearerトークンの検証
@dataclass
class AuthenticationResponse:
    auth_type: Literal["bearer", "session"]
    message: str
    payload: dict | None = None


# Bearerトークンのためのセキュリティスキーム
bearer_scheme = HTTPBearer(auto_error=False)


# トークンを検証するヘルパー関数
def validate_bearer_token(authorization: HTTPAuthorizationCredentials):
    if authorization and authorization.credentials == BEARER_TOKEN:
        return AuthenticationResponse(auth_type="bearer", message="Authenticated with Bearer token")
    return None


def verify_bearer_token(
        authorization: HTTPAuthorizationCredentials = Security(bearer_scheme)
) -> AuthenticationResponse:
    result = validate_bearer_token(authorization)
    if result:
        return result
    raise CustomHTTPException(status_code=401, detail="Invalid or missing Bearer token")


# JWTトークンの検証
async def verify_session(request: Request) -> AuthenticationResponse:
    user = request.session.get("user_info")
    guild_id = request.path_params.get("guild_id")
    if user:
        if guild_id:
            if not (await get_guild(int(user["id"]), guild_id)):
                raise CustomHTTPException(status_code=404,
                                          detail="Guild does not exist or user does not have access to it")
        return AuthenticationResponse(auth_type="session", message="Authenticated with session", payload=user)
    raise CustomHTTPException(status_code=401, detail="Invalid or missing session")


# BearerトークンまたはJWTトークンの検証
async def verify_all_tokens(
        request: Request,
        authorization: HTTPAuthorizationCredentials = Security(bearer_scheme)
) -> AuthenticationResponse:
    result = validate_bearer_token(authorization) or await verify_session(request)
    if result:
        return result
    raise CustomHTTPException(status_code=401, detail="Invalid or missing Bearer/Session token")


async def verify_turnstile_token(token: str) -> bool | None:
    """
    Verify a Cloudflare Turnstile token.

    Args:
        token: The turnstile token to verify

    Returns:
        bool: True if the token is valid, False otherwise
    """
    if not TURNSTILE_SECRET_KEY:
        # If no secret key is configured, skip verification (for development)
        return True

    async with aiohttp.ClientSession() as session:
        response = await session.post(
            "https://challenges.cloudflare.com/turnstile/v0/siteverify",
            data={
                "secret": TURNSTILE_SECRET_KEY,
                "response": token
            }
        )
        result = await response.json()
        if not result.get("success", False):
            raise CustomHTTPException(status_code=400, detail="Invalid Turnstile token")
        return None
