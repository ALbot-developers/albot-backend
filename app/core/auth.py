from dataclasses import dataclass
from typing import Literal

from fastapi import Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.constants import BEARER_TOKEN
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
