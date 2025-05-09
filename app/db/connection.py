import asyncpg

from app import constants

_connection_pool = None


async def create_connection_pool():
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = await asyncpg.create_pool(
            user="postgres",
            database=constants.DB_DATABASE,
            host=constants.DB_HOST,
            min_size=5,
            max_size=15
        )
    return _connection_pool


def get_connection_pool():
    return _connection_pool
