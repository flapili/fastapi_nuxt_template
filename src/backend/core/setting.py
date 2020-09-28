import os
from enum import IntEnum
from functools import lru_cache
import logging
from typing import Union, List


from pydantic import PostgresDsn, RedisDsn, BaseSettings, Field


try:
    workers: int = len(os.sched_getaffinity(0))
except AttributeError:
    import multiprocessing
    workers: int = multiprocessing.cpu_count()

if workers < 2:
    workers = 2


class redisDBenum(IntEnum):
    session = 0


class GunicornSetting(BaseSettings):
    PORT: int = Field(80, gt=0, lt=2 ** 16)
    WORKER: int = Field(workers, gt=1)
    WORKER_CLASS: str = "uvicorn.workers.UvicornWorker"
    BIND: Union[str, List[str]] = ":80"
    WORKER_TMP_DIR: str = "/dev/shm"
    LOG_FILE: str = "-"


class Setting(BaseSettings):
    gunicorn: GunicornSetting = GunicornSetting()

    logging_lever: int = logging.DEBUG
    PSQL_URL: PostgresDsn
    REDIS_URL: RedisDsn
    COOKIE_DOMAIN: str
    session_ttl: int = 60 * 60 * 6


@lru_cache()
def get_setting() -> Setting:
    return Setting()
