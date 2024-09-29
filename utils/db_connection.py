import asyncpg

_connection_pool = None


async def create_connection_pool():
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = await asyncpg.create_pool(
            user="postgres",
            database="postgres",
            host="100.121.195.21",
            min_size=2,
            max_size=10
        )
    return _connection_pool


def get_connection_pool():
    return _connection_pool