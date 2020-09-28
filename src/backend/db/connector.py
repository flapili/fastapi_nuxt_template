# coding: utf-8
from fastapi import Depends

import aioredis
from databases import Database

from core.setting import Setting, get_setting


db = Database(get_setting().PSQL_URL)


class get_redis:
    def __init__(self, db: int = 0):
        self.db = db

    async def __call__(self, setting: Setting = Depends(get_setting)):
        redis_conn = await aioredis.create_redis(setting.REDIS_URL, db=self.db)
        try:
            yield redis_conn
        finally:
            redis_conn.close()
            await redis_conn.wait_closed()
