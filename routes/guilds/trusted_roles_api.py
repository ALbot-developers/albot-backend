from dataclasses import dataclass
from typing import List

import asyncpg
from fastapi import APIRouter, Security

from utils.auth import verify_token
from utils.db_connection import get_connection_pool

router = APIRouter()


@dataclass
class TrustedRolesData:
    is_enabled: bool = None
    role_ids: List[int] = None


@dataclass
class TrustedRolesDataResponse:
    message: str
    data: TrustedRolesData


@router.get("/{guild_id}/trusted_roles", response_model=TrustedRolesDataResponse)
async def get_guild_trusted_roles(guild_id: int, _auth=Security(lambda: verify_token("all"))):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        row = await conn.fetchrow('SELECT is_enabled, role_ids FROM trusted_roles WHERE guild_id = $1', guild_id)
        data = TrustedRolesData(
            is_enabled=row['is_enabled'],
            role_ids=row['role_ids']
        )
    return TrustedRolesDataResponse(
        message="Fetched trusted roles settings.",
        data=data
    )


@router.put("/{guild_id}/trusted_roles")
async def update_guild_trusted_roles(guild_id: int, data: TrustedRolesData, _auth=Security(lambda: verify_token("all"))):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを更新
        # is_enabledとrole_idsがnullでない場合のみそれぞれ更新
        await conn.execute(
            '''
            UPDATE trusted_roles
            SET 
                is_enabled = CASE WHEN $1 IS NOT NULL THEN $1 ELSE is_enabled END,
                role_ids = CASE WHEN $2 IS NOT NULL THEN $2 ELSE role_ids END
            WHERE guild_id = $3
            ''',
            data.is_enabled, data.role_ids, guild_id
        )
    return {
        "message": "Updated trusted roles settings."
    }
