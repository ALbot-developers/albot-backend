from contextlib import asynccontextmanager

import sentry_sdk
import stripe
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app import constants
from app.db.connection import create_connection_pool
from app.routes.guilds import router as guilds
from app.routes.metrics import router as metrics
from app.routes.oauth2 import router as oauth2
from app.routes.shards import router as shards
from app.routes.users import router as users
from app.routes.webhooks import router as webhooks


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
sentry_sdk.init(
    dsn=constants.SENTRY_DSN,
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
    environment=constants.SENTRY_ENV,
)
app = FastAPI(lifespan=lifespan, root_path=f"/{API_VERSION}")
# noinspection PyTypeChecker
app.add_middleware(SessionMiddleware, secret_key=constants.SESSION_SECRET, domain=constants.SESSION_DOMAIN)
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://mypage.albot.info", "https://albot.info"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(oauth2.router, prefix="/oauth2", tags=["oauth2"])
app.include_router(shards.router, prefix="/shards", tags=["shards"])
app.include_router(guilds.router, prefix="/guilds", tags=["guilds"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(metrics.router, prefix="/metrics", tags=["metrics"])
app.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])


@app.get("/")
async def root():
    return {"message": "Running."}
