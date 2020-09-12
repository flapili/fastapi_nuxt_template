# coding: utf-8

from backend.core.config import get_config, Config

# we assume all values are already checked by pydantic,
# but we use get_config to avoid any mutation.
_config: Config = get_config()


workers = _config.gunicorn.WORKER
worker_class = _config.gunicorn.WORKER_CLASS
bind = _config.gunicorn.BIND
worker_tmp_dir = _config.gunicorn.WORKER_TMP_DIR
log_file = _config.gunicorn.LOG_FILE
