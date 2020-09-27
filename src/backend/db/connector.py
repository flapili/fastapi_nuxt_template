# coding: utf-8
from fastapi import Depends

import aioredis
from databases import Database

from backend.core.config import Config, get_config


db = Database(get_config().PSQL_URL)


class get_redis:
    def __init__(self, db: int = 0):
        self.db = db

    async def __call__(self, config: Config = Depends(get_config)):
        redis_conn = await aioredis.create_redis(config.REDIS_URL, db=self.db)
        try:
            yield redis_conn
        finally:
            redis_conn.close()
            await redis_conn.wait_closed()
