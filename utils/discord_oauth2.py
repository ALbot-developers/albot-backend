from typing import Tuple

import aiohttp

import envs
from type_specifications.discord_api import UserPIIResponse

DISCORD_BASE_URL = 'https://discord.com/api'


def get_oauth2_url(redirect_uri, state):
    return (
        f"https://discord.com/oauth2/authorize"
        f"?client_id=727508841368911943"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=identify%20guilds"
        f"&state={state}"
        f"&prompt=none"
    )


async def get_user_info(access_token) -> UserPIIResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get(DISCORD_BASE_URL + '/users/@me',
                               headers={'Authorization': f'Bearer {access_token}'}) as res_info:
            res_dict = await res_info.json()
            return UserPIIResponse.from_json(res_dict)


async def exchange_code(code, redirect_url) -> Tuple[str, str]:
    data = {
        'client_id': envs.DISCORD_CLIENT_ID,
        'client_secret': envs.DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_url,
        'scope': 'identify guilds'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{DISCORD_BASE_URL}/oauth2/token', data=data, headers=headers) as r:
            r.raise_for_status()
            res_json = await r.json()
            return res_json['access_token'], res_json['refresh_token']


async def refresh_code(refresh_token):
    data = {
        'client_id': envs.DISCORD_CLIENT_ID,
        'client_secret': envs.DISCORD_CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'scope': 'identify guilds'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{DISCORD_BASE_URL}/oauth2/token', data=data, headers=headers) as r:
            r.raise_for_status()
            return await r.json()
