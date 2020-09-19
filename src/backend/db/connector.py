from functools import lru_cache

from databases import Database

from backend.core.config import config


@lru_cache
async def get_db():
    return Database(config.PSQL_URL)
