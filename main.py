from contextlib import asynccontextmanager

import stripe
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

import constants
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
stripe.api_key = constants.STRIPE_SECRET_KEY

app = FastAPI(lifespan=lifespan, root_path=f"/{API_VERSION}")
# noinspection PyTypeChecker
app.add_middleware(SessionMiddleware, secret_key=constants.SESSION_SECRET, domain="localhost", same_site="none")
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://mypage.albot.info"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(oauth2.router, prefix=f"/oauth2", tags=["oauth2"])
app.include_router(shards.router, prefix=f"/shards", tags=["shards"])
app.include_router(guilds.router, prefix=f"/guilds", tags=["guilds"])
app.include_router(users.router, prefix=f"/users", tags=["users"])
app.include_router(metrics.router, prefix=f"/metrics", tags=["metrics"])


@app.get("/")
async def root():
    return {"message": "Running."}
