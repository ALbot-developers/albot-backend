from dataclasses import dataclass
from typing import Optional, Literal

from fastapi import Security, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from constants import BEARER_TOKEN
from services.user import get_user_guild


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
    raise HTTPException(status_code=401, detail="Invalid or missing Bearer token")


# JWTトークンの検証
async def verify_session(request: Request, guild_id: Optional['int'] = None) -> AuthenticationResponse:
    user = request.session.get("user_info")
    if user:
        if guild_id:
            if not (await get_user_guild(int(user["id"]), guild_id)):
                raise HTTPException(status_code=404, detail="Guild does not exist or user does not have access to it")
        return AuthenticationResponse(auth_type="session", message="Authenticated with session", payload=user)
    raise HTTPException(status_code=401, detail="Invalid or missing session")


# BearerトークンまたはJWTトークンの検証
async def verify_all_tokens(
        request: Request,
        authorization: HTTPAuthorizationCredentials = Security(bearer_scheme),
        guild_id: Optional['int'] = None
) -> AuthenticationResponse:
    result = validate_bearer_token(authorization) or await verify_session(request, guild_id)
    if result:
        return result
    raise HTTPException(status_code=401, detail="Invalid or missing Bearer/Session token")
