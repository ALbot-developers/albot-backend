from typing import List

import aiohttp

from type_specifications.discord_api import PartialGuild, UserPIIResponse

DISCORD_BASE_URL = 'https://discord.com/api/v10'


async def get_user_guilds(access_token: str) -> List[PartialGuild]:
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
