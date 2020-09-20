from functools import lru_cache

from databases import Database

from backend.core.config import config


db = Database(config.PSQL_URL)


@lru_cache
def get_db():
    return Database(config.PSQL_URL)
