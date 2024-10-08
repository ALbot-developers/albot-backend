from uuid import uuid4

from fastapi import APIRouter, Request

from utils.discord_oauth2 import get_oauth2_url, exchange_code, get_user_info

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
async def oauth2_callback(code: str, state: str, request: Request):
    if state != request.session.get("state"):
        return {"error": "Invalid state"}
    redirect = request.session["redirect"]
    del request.session["state"], request.session["redirect"]
    access_token, refresh_token = await exchange_code(code, redirect)
    request.session["access_token"] = access_token
    request.session["refresh_token"] = refresh_token
    user_info = await get_user_info(access_token)
    request.session["user_info"] = user_info.to_dict()
    return {
        "message": "Logged in."
    }
