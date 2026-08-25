import asyncpg
import os

#   psql -U admin -d lab7_db

_pool: asyncpg.Pool | None = None

async def init_pool():
    global _pool
    _pool = await asyncpg.create_pool(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", 5432)),
        database=os.getenv("DB_NAME", "lab7_db"),
        user=os.getenv("DB_USER", "admin"),
        password=os.getenv("DB_PASSWORD", ""),
    )
    return _pool

async def get_pool() -> asyncpg.Pool:
    return _pool