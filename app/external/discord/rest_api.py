from typing import List

import aiohttp

from app.constants import DISCORD_REPORT_CH_WEBHOOK_URL
from app.external.discord.models import PartialGuild, UserPIIResponse

DISCORD_BASE_URL = 'https://discord.com/api/v10'


async def fetch_user_guilds(access_token: str) -> List[PartialGuild]:
    url = f"{DISCORD_BASE_URL}/users/@me/guilds"
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            res = await response.json()
            return [PartialGuild.from_dict(guild) for guild in res]


async def get_user_info(access_token) -> UserPIIResponse:
    async with aiohttp.ClientSession() as session:
        async with session.get(DISCORD_BASE_URL + '/users/@me',
                               headers={'Authorization': f'Bearer {access_token}'}) as res_info:
            res_dict = await res_info.json()
            return UserPIIResponse.from_dict(res_dict)


async def push_webhook(content: dict | list):
    async with aiohttp.ClientSession() as session:
        async with session.post(DISCORD_REPORT_CH_WEBHOOK_URL, json=content) as res:
            res.raise_for_status()
            return res.status == 204
