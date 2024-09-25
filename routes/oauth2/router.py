import urllib.parse
from uuid import uuid4

from fastapi import APIRouter, Request
from starlette.responses import RedirectResponse

from utils.discord_oauth2 import get_oauth2_url, exchange_code, get_user_info

router = APIRouter()


@router.get("/login")
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


@router.get("/callback")
async def oauth2_callback(code: str, state: str, request: Request):
    if state != request.session.get("state"):
        return {"error": "Invalid state"}
    redirect = request.session.get("redirect", "/")
    del request.session["state"], request.session["redirect"]
    access_token, refresh_token = await exchange_code(code, router.url_path_for("oauth2_callback"))
    request.session["access_token"] = access_token
    request.session["refresh_token"] = refresh_token
    user_info = await get_user_info(access_token)
    request.session["user_info"] = user_info.to_json()
    return RedirectResponse(redirect)
