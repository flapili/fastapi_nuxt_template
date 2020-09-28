# coding: utf-8

from backend.core.setting import get_setting

workers = get_setting().gunicorn.WORKER
worker_class = get_setting().gunicorn.WORKER_CLASS
bind = get_setting().gunicorn.BIND
worker_tmp_dir = get_setting().gunicorn.WORKER_TMP_DIR
log_file = get_setting().gunicorn.LOG_FILE
