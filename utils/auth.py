import jwt
from fastapi import Security, HTTPException, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from envs import BEARER_TOKEN
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


def validate_jwt_token(jwt_token: str):
    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
            return AuthenticationResponse(auth_type="jwt", message="Authenticated with JWT token", payload=payload)
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="JWT token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid JWT token")
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
def verify_jwt_token(
        jwt_token: str = Cookie(None)
) -> AuthenticationResponse:
    result = validate_jwt_token(jwt_token)
    if result:
        return result
    raise HTTPException(status_code=403, detail="Invalid or missing JWT token")


# BearerトークンまたはJWTトークンの検証
def verify_all_tokens(
        authorization: HTTPAuthorizationCredentials = Security(bearer_scheme),
        jwt_token: str = Cookie(None)
) -> AuthenticationResponse:
    result = validate_bearer_token(authorization) or validate_jwt_token(jwt_token)
    if result:
        return result
    raise HTTPException(status_code=403, detail="Invalid or missing Bearer/JWT token")
