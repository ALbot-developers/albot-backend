import asyncpg

connection_pool = None


async def create_db_pool():
    global connection_pool
    connection_pool = await asyncpg.create_pool(
        user="postgres",
        database="postgres",
        host="100.121.195.21",
        min_size=2,
        max_size=10
    )
    return connection_pool
