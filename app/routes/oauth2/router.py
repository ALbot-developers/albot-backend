from uuid import uuid4

from aiohttp import ClientResponseError
from fastapi import APIRouter, Request, Response

from app.external import discord
from app.schemas.api_response import PlainAPIResponse, Oauth2APIResponse
from app.schemas.oauth2 import AuthURL
from app.services import user

router = APIRouter()


@router.get("/login", response_model=Oauth2APIResponse)
async def oauth2_redirect(request: Request, redirect: str):
    state = str(uuid4())[0:8]
    request.session["state"] = state
    request.session["redirect"] = redirect
    url = discord.oauth2.get_url(
        redirect, state
    )
    return Oauth2APIResponse(
        message="Redirecting to OAuth2 login.",
        data=AuthURL(url=url)
    )


@router.post("/callback", response_model=PlainAPIResponse)
async def oauth2_callback(code: str, state: str, response: Response, request: Request):
    if state != request.session.get("state"):
        response.status_code = 400
        return {"error": "Invalid state"}
    redirect = request.session["redirect"]
    del request.session["state"], request.session["redirect"]
    try:
        access_token, refresh_token = await discord.oauth2.exchange_code(code, redirect)
    except ClientResponseError:
        response.status_code = 400
        return {"error": "Invalid code"}
    request.session["access_token"] = access_token
    request.session["refresh_token"] = refresh_token
    user_info = await discord.rest_api.get_user_info(access_token)
    request.session["user_info"] = user_info.to_dict()
    user_guilds = await discord.rest_api.fetch_user_guilds(access_token)
    await user.store_guilds(int(user_info.id), user_guilds)
    return PlainAPIResponse(
        message="Logged in."
    )


@router.post("/logout", response_model=PlainAPIResponse)
async def logout(request: Request):
    request.session.clear()
    return PlainAPIResponse(
        message="Logged out."
    )
