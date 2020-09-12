# syntax = docker/dockerfile:experimental


FROM python:3.8-slim-buster AS api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD src/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# RUN pip install -r requirements.txt
# RUN --mount=type=cache,target=.cache/pip pip install -r requirements.txt

WORKDIR /app
# ADD src/alembic.ini /app/alembic.ini
ADD src/backend /app/backend

ENTRYPOINT ["gunicorn", "backend.core.app:app", "-c", "backend/gunicorn_conf.py"]

# EXPOSE 8080

# FROM api AS db_migration

# WORKDIR /app/migrations
# ADD src/migrations /app/migrations
# ENTRYPOINT []
# CMD ["true"]