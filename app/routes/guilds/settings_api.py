import asyncpg
from fastapi import APIRouter, Security, HTTPException, Depends

from app.core.auth import verify_all_tokens
from app.core.dependencies import get_subscription
from app.db.connection import get_connection_pool
from app.models.settings import PremiumSettings
from app.models.subscription import Subscription
from app.schemas.api_data import GuildSettingsData
from app.schemas.api_response import GuildSettingsAPIResponse, PlainAPIResponse
from app.schemas.guild_settings import GuildSettingsUpdate
from app.services import guild_settings
from app.services.guild_settings import get_default

router = APIRouter()


@router.get("/{guild_id}/settings", response_model=GuildSettingsAPIResponse)
async def get_guild_settings_api(guild_id: int, subscription: Subscription = Depends(get_subscription),
                                 _auth=Security(verify_all_tokens)):
    settings = await guild_settings.get(guild_id)
    if subscription is None:
        default_settings = await get_default()
        for key in PremiumSettings.__annotations__.keys():
            if key not in settings.__dict__:
                continue
            setattr(settings, key, getattr(default_settings, key))
    return GuildSettingsAPIResponse(
        message="Fetched guild data.",
        data=GuildSettingsData(
            settings=settings
        )
    )


@router.post("/{guild_id}/settings", response_model=PlainAPIResponse)
async def update_guild_settings(guild_id: int, settings: GuildSettingsUpdate,
                                subscription: Subscription = Depends(get_subscription),
                                _auth=Security(verify_all_tokens)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # get all attributes with values
        attributes = {k: (None if v == "" else v) for k, v in settings.__dict__.items() if v is not None}
        if not attributes:
            raise HTTPException(status_code=400, detail="No settings data provided.")
        # if subscription is None and PremiumSettings in attributes, return an error
        if subscription is None:
            if any(k in attributes for k in PremiumSettings.__annotations__.keys()):
                raise HTTPException(status_code=403, detail="Requires premium subscription.")
        if 'character_limit' in attributes:
            # replace to word_limit
            # todo: DBのカラム名をcharacter_limitに変更する
            attributes['word_limit'] = attributes.pop('character_limit')
        query = (
            f"INSERT INTO settings_data (guild_id, {', '.join(attributes.keys())}) "
            f"VALUES ({guild_id}, {', '.join([f'${i + 1}' for i in range(len(attributes))])}) "
            f"ON CONFLICT (guild_id) DO UPDATE SET "
            f"{', '.join([f'{k} = EXCLUDED.{k}' for k in attributes.keys()])}"
        )
        # execute the query with the values
        await conn.execute(query, *attributes.values())
    return PlainAPIResponse(
        message="Updated guild data."
    )


@router.delete("/{guild_id}/settings", response_model=PlainAPIResponse)
async def delete_guild_settings(guild_id: int, _auth=Security(verify_all_tokens)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute('DELETE FROM settings_data WHERE guild_id = $1;', guild_id)
        await conn.execute("INSERT INTO settings_data (guild_id) VALUES ($1) ON CONFLICT DO NOTHING", guild_id)
    return PlainAPIResponse(
        message="Deleted guild data."
    )
