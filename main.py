from contextlib import asynccontextmanager

import stripe
from fastapi import FastAPI, Response
from starlette.middleware.sessions import SessionMiddleware

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

API_VERSION = "v2"
stripe.api_key = envs.STRIPE_SECRET_KEY

app = FastAPI(lifespan=lifespan, root_path=f"/{API_VERSION}")
# noinspection PyTypeChecker
app.add_middleware(SessionMiddleware, secret_key=envs.SESSION_SECRET)
app.include_router(oauth2.router, prefix=f"/oauth2", tags=["oauth2"])
app.include_router(shards.router, prefix=f"/shards", tags=["shards"])
app.include_router(guilds.router, prefix=f"/guilds", tags=["guilds"])
app.include_router(users.router, prefix=f"/users", tags=["users"])
app.include_router(metrics.router, prefix=f"/metrics", tags=["metrics"])


@app.get("/{_full_path:path}")
async def api_not_found(response: Response, _full_path: str):
    response.status_code = 404
    return {"message": "Endpoint not found."}
