import json

import asyncpg

from app.db.connection import get_connection_pool
from app.models.trusted_roles import TrustedRoles


async def get(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        row = await conn.fetchrow('SELECT is_enabled, role_ids FROM trusted_roles WHERE guild_id = $1', guild_id)
        if row:
            return TrustedRoles(
                enabled=row['is_enabled'],
                role_ids=json.loads(row['role_ids'])
            )
        else:
            return TrustedRoles(
                enabled=False,
                role_ids=[]
            )


async def update(guild_id: int, enabled: bool | None, role_ids: list[int] | None):
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
            enabled, role_ids, guild_id
        )
