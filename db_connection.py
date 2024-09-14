import asyncpg

connection_pool = None


async def get_connection_pool():
    global connection_pool
    if connection_pool is None:
        connection_pool = await asyncpg.create_pool(
            user="postgres",
            database="postgres",
            host="100.121.195.21",
            min_size=2,
            max_size=10
        )
    return connection_pool
