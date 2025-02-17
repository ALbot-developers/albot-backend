from typing import Tuple

import aiohttp

import constants

DISCORD_BASE_URL = 'https://discord.com/api/v10'


def get_oauth2_url(redirect_uri, state):
    return (
        f"https://discord.com/oauth2/authorize"
        f"?client_id={constants.DISCORD_CLIENT_ID}"
        f"&redirect_uri={redirect_uri}"
        f"&response_type=code"
        f"&scope=identify%20guilds"
        f"&state={state}"
        f"&prompt=none"
    )


async def exchange_code(code, redirect_url) -> Tuple[str, str]:
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_url,
        'scope': 'identify guilds'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f'{DISCORD_BASE_URL}/oauth2/token', data=data, headers=headers,
                                auth=aiohttp.BasicAuth(constants.DISCORD_CLIENT_ID,
                                                       constants.DISCORD_CLIENT_SECRET)) as r:
            r.raise_for_status()
            res_json = await r.json()
            return res_json['access_token'], res_json['refresh_token']


async def refresh_code(refresh_token):
    data = {
        'client_id': constants.DISCORD_CLIENT_ID,
        'client_secret': constants.DISCORD_CLIENT_SECRET,
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
