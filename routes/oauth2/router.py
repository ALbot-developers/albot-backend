import datetime
import json
from uuid import uuid4

import asyncpg
from fastapi import APIRouter, Request, Response

from utils.db_connection import get_connection_pool
from utils.discord_api import fetch_user_guilds, get_user_info
from utils.discord_oauth2 import get_oauth2_url, exchange_code

router = APIRouter()


@router.get("/login")
async def oauth2_redirect(request: Request, redirect: str):
    state = str(uuid4())[0:8]
    request.session["state"] = state
    request.session["redirect"] = redirect
    url = get_oauth2_url(
        redirect, state
    )
    return {
        "message": "Redirecting to OAuth2 login.",
        "data": {
            "url": url
        }
    }


@router.post("/callback")
async def oauth2_callback(code: str, state: str, response: Response, request: Request):
    if state != request.session.get("state"):
        response.status_code = 400
        return {"error": "Invalid state"}
    redirect = request.session["redirect"]
    del request.session["state"], request.session["redirect"]
    access_token, refresh_token = await exchange_code(code, redirect)
    request.session["access_token"] = access_token
    request.session["refresh_token"] = refresh_token
    user_info = await get_user_info(access_token)
    request.session["user_info"] = user_info.to_dict()
    user_guilds = [guild.to_dict() for guild in await fetch_user_guilds(access_token)]
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute(
            'INSERT INTO user_guilds (user_id, guilds, updated_at) VALUES ($1, $2, $3) '
            'ON CONFLICT (user_id) DO UPDATE SET guilds = $2, updated_at = $3',
            int(user_info.id), json.dumps(user_guilds), datetime.datetime.now()
        )
    return {
        "message": "Logged in."
    }


@router.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return {
        "message": "Logged out."
    }
