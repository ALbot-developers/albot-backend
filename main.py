from contextlib import asynccontextmanager
from uuid import uuid4
import urllib.parse

from fastapi import FastAPI, Response

from db_connection import create_db_pool
from routes import shards
from sessions import SessionData, get_verifier, get_cookie


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # アプリケーションが起動する際に接続プールを作成
    pool = await create_db_pool()
    try:
        yield  # アプリケーションが実行されている間
    finally:
        # アプリケーションが終了する際に接続プールを閉じる
        await pool.close()

app = FastAPI()

API_VERSION = "v2"
ENDPOINT_PREFIX = f"/api/{API_VERSION}"

app = FastAPI(debug=True, lifespan=lifespan)


@app.get("/")
async def root():
    return {"status": "running"}


@app.get("/oauth2/url")
async def get_oauth2_url(response: Response):
    session = uuid4()
    state = str(uuid4())[0:8]
    data = SessionData(oauth2_state=state)
    verifier = get_verifier()
    await verifier.backend.create(session, data)
    cookie = get_cookie()
    cookie.attach_to_response(response, session)
    return {
        "url": f"https://discord.com/oauth2/authorize"
               f"?client_id=727508841368911943"
               f"&redirect_uri={urllib.parse.quote(app.url_path_for('oauth2_callback'))}"
               f"&response_type=code"
               f"&scope=identify%20guilds"
               f"&state={state}"
               f"&prompt=none"
    }


@app.get("/oauth2/callback")
async def oauth2_callback(code: str):
    # set jwt token
    return {"code": code}
