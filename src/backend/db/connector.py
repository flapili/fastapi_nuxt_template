from databases import Database

from backend.core.config import config

db = Database(config.PSQL_URL)
