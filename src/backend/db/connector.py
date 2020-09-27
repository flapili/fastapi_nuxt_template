# coding: utf-8
from fastapi import Depends

import aioredis
from databases import Database

from backend.core.config import config, get_config


db = Database(get_config().PSQL_URL)


class get_redis_conn:
    def __init__(self, db: int = 0, config: config = Depends(get_config)):
        self.db = db

    async def __call__(self):
        redis_conn = await aioredis.create_connection(config.REDIS_URL, db=self.db)
        try:
            yield redis_conn
        finally:
            redis_conn.close()
            await redis_conn.wait_closed()
