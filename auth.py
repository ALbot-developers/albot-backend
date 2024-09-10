from typing import Literal

from fastapi import Security, HTTPException, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

# 固定のBearerトークン
FIXED_BEARER_TOKEN = "your_fixed_token"

# JWTシークレットキー
SECRET_KEY = "your_jwt_secret"
ALGORITHM = "HS256"

# Bearerトークンのためのセキュリティスキーム
bearer_scheme = HTTPBearer(auto_error=False)


# トークンを検証するヘルパー関数
def validate_bearer_token(authorization: HTTPAuthorizationCredentials):
    if authorization and authorization.credentials == FIXED_BEARER_TOKEN:
        return {"auth_type": "bearer", "message": "Authenticated with Bearer token"}
    return None


def validate_jwt_token(jwt_token: str):
    if jwt_token:
        try:
            payload = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
            return {"auth_type": "jwt", "message": "Authenticated with JWT", "payload": payload}
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=403, detail="JWT token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=403, detail="Invalid JWT token")
    return None


# 認証のための関数
def verify_token(
        auth_method: Literal["bearer", "jwt", "all"],
        authorization: HTTPAuthorizationCredentials = Security(bearer_scheme),
        jwt_token: str = Cookie(None)
):
    """
    認証方法に基づいてBearerトークンまたはJWTトークンを検証します。

    :param auth_method: 使用する認証方法 ("bearer", "jwt", "all")
    :param authorization: Authorizationヘッダー (Bearerトークン)
    :param jwt_token: Cookie内のJWTトークン
    """
    if auth_method == "bearer":
        result = validate_bearer_token(authorization)
    elif auth_method == "jwt":
        result = validate_jwt_token(jwt_token)
    elif auth_method == "all":
        result = validate_bearer_token(authorization) or validate_jwt_token(jwt_token)
    else:
        raise HTTPException(status_code=403, detail="Unsupported authentication method")

    if result:
        return result

    # 認証に失敗した場合
    raise HTTPException(status_code=403, detail="Invalid or missing Bearer/JWT token")
