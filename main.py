import os
from contextlib import asynccontextmanager

import stripe
from fastapi import FastAPI, Response
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

import envs
from routes.guilds import router as guilds
from routes.metrics import router as metrics
from routes.oauth2 import router as oauth2
from routes.shards import router as shards
from routes.users import router as users
from utils.db_connection import create_connection_pool


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # アプリケーションが起動する際に接続プールを作成
    pool = await create_connection_pool()
    try:
        yield  # アプリケーションが実行されている間
    finally:
        # アプリケーションが終了する際に接続プールを閉じる
        await pool.close()


def generate_react_response(response: Response):
    index_path = os.path.join("public", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    else:
        response.status_code = 404
        response.body = "Index file not found"
        return response


API_VERSION = "v2"
ENDPOINT_PREFIX = f"/api/{API_VERSION}"

stripe.api_key = envs.STRIPE_SECRET_KEY

app = FastAPI(lifespan=lifespan)
app.mount("/assets", StaticFiles(directory="public/assets"), name="assets")
# noinspection PyTypeChecker
app.add_middleware(SessionMiddleware, secret_key=envs.SESSION_SECRET)
app.include_router(oauth2.router, prefix=f"{ENDPOINT_PREFIX}/oauth2", tags=["oauth2"])
app.include_router(shards.router, prefix=f"{ENDPOINT_PREFIX}/shards", tags=["shards"])
app.include_router(guilds.router, prefix=f"{ENDPOINT_PREFIX}/guilds", tags=["guilds"])
app.include_router(users.router, prefix=f"{ENDPOINT_PREFIX}/users", tags=["users"])
app.include_router(metrics.router, prefix=f"{ENDPOINT_PREFIX}/metrics", tags=["metrics"])


@app.get("/{_full_path:path}")
async def serve_app(response: Response, _full_path: str):
    return generate_react_response(response)
