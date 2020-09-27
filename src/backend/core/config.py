import os
from functools import lru_cache
import logging
from typing import Union, List, Any


from pydantic import PostgresDsn, RedisDsn, BaseSettings, Field


try:
    workers: int = len(os.sched_getaffinity(0))
except AttributeError:
    import multiprocessing
    workers: int = multiprocessing.cpu_count()

if workers < 2:
    workers = 2


class GunicornConfig(BaseSettings):
    PORT: int = Field(80, gt=0, lt=2 ** 16)
    WORKER: int = Field(workers, gt=1)
    WORKER_CLASS: str = "uvicorn.workers.UvicornWorker"
    BIND: Union[str, List[str]] = ":80"
    WORKER_TMP_DIR: str = "/dev/shm"
    LOG_FILE: str = "-"


class Config(BaseSettings):
    gunicorn: GunicornConfig = GunicornConfig()

    logging_lever: int = logging.DEBUG
    PSQL_URL: PostgresDsn
    REDIS_URL: RedisDsn
    COOKIE_DOMAIN: str


@lru_cache()
def get_config(*args: Any, **kwargs: Any) -> Config:
    return Config(*args, **kwargs)


config: Config = get_config()
