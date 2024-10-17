from fastapi import Security, HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from constants import BEARER_TOKEN
from type_specifications.auth import AuthenticationResponse

# JWTシークレットキー
SECRET_KEY = "your_jwt_secret"
ALGORITHM = "HS256"

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
def verify_session(request: Request) -> AuthenticationResponse:
    user = request.session.get("user_info")
    if user:
        return AuthenticationResponse(auth_type="session", message="Authenticated with session", payload=user)
    raise HTTPException(status_code=403, detail="Invalid or missing session")


# BearerトークンまたはJWTトークンの検証
def verify_all_tokens(
        request: Request,
        authorization: HTTPAuthorizationCredentials = Security(bearer_scheme)
) -> AuthenticationResponse:
    result = validate_bearer_token(authorization) or verify_session(request)
    if result:
        return result
    raise HTTPException(status_code=403, detail="Invalid or missing Bearer/JWT token")
