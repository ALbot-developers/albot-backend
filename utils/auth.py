from typing import Optional

from fastapi import Security, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from constants import BEARER_TOKEN
from type_specifications.auth import AuthenticationResponse
from utils.others import get_user_guild

# Bearerトークンのためのセキュリティスキーム
bearer_scheme = HTTPBearer(auto_error=False)


# トークンを検証するヘルパー関数
def validate_bearer_token(authorization: HTTPAuthorizationCredentials):
    if authorization and authorization.credentials == BEARER_TOKEN:
        return AuthenticationResponse(auth_type="bearer", message="Authenticated with Bearer token")
    return None


# Bearerトークンの検証
def verify_bearer_token(
        authorization: HTTPAuthorizationCredentials = Security(bearer_scheme)
) -> AuthenticationResponse:
    result = validate_bearer_token(authorization)
    if result:
        return result
    raise HTTPException(status_code=403, detail="Invalid or missing Bearer token")


# JWTトークンの検証
async def verify_session(request: Request, guild_id: Optional['int'] = None) -> AuthenticationResponse:
    user = request.session.get("user_info")
    if user:
        if guild_id:
            if not (await get_user_guild(int(user["id"]), guild_id)):
                raise HTTPException(status_code=403, detail="User is not in the guild")
        return AuthenticationResponse(auth_type="session", message="Authenticated with session", payload=user)
    raise HTTPException(status_code=403, detail="Invalid or missing session")


# BearerトークンまたはJWTトークンの検証
async def verify_all_tokens(
        request: Request,
        authorization: HTTPAuthorizationCredentials = Security(bearer_scheme),
        guild_id: Optional['int'] = None
) -> AuthenticationResponse:
    result = validate_bearer_token(authorization) or await verify_session(request, guild_id)
    if result:
        return result
    raise HTTPException(status_code=403, detail="Invalid or missing Bearer/JWT token")
