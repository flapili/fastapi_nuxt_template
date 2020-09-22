# coding: utf-8
from pathlib import Path
from importlib import import_module

from fastapi import FastAPI

from backend.db.connector import db

app = FastAPI(root_path="/api/")

for file in Path("./backend/router").glob("*.py"):
    if file.stem != "__init__":
        module = import_module(".".join(file.parts[:-1] + (file.stem,)))
        app.include_router(
            module.router, prefix=f"/{file.stem}", tags=[file.stem],
        )


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
