import urllib.parse
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import RedirectResponse

import envs
from db_connection import create_connection_pool
from oauth2 import exchange_code, get_user_info, get_oauth2_url
from routes.guilds import router as guilds
from routes.shards import router as shards


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # アプリケーションが起動する際に接続プールを作成
    pool = await create_connection_pool()
    try:
        yield  # アプリケーションが実行されている間
    finally:
        # アプリケーションが終了する際に接続プールを閉じる
        await pool.close()


API_VERSION = "v2"
ENDPOINT_PREFIX = f"/api/{API_VERSION}"

app = FastAPI(debug=True, lifespan=lifespan)
# noinspection PyTypeChecker
app.add_middleware(SessionMiddleware, secret_key=envs.SESSION_SECRET)
app.include_router(shards.router, prefix=f"{ENDPOINT_PREFIX}/shards", tags=["shards"])
app.include_router(guilds.router, prefix=f"{ENDPOINT_PREFIX}/guilds", tags=["guilds"])


@app.get("/")
async def root():
    return {"status": "running"}


@app.get("/oauth2/login")
async def oauth2_redirect(request: Request):
    state = str(uuid4())[0:8]
    request.session["state"] = state
    request.session["redirect"] = request.query_params.get("redirect", "/")
    url = get_oauth2_url(
        urllib.parse.quote(
            str(request.url_for("oauth2_callback", _external=True))
        ), state
    )
    return RedirectResponse(url)


@app.get("/oauth2/callback")
async def oauth2_callback(code: str, state: str, request: Request):
    if state != request.session.get("state"):
        return {"error": "Invalid state"}
    redirect = request.session.get("redirect", "/")
    del request.session["state"], request.session["redirect"]
    access_token, refresh_token = await exchange_code(code, app.url_path_for("oauth2_callback"))
    request.session["access_token"] = access_token
    request.session["refresh_token"] = refresh_token
    user_info = await get_user_info(access_token)
    request.session["user_info"] = user_info.to_json()
    return RedirectResponse(redirect)
