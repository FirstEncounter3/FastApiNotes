from contextlib import asynccontextmanager

from fastapi import FastAPI

from routes.router import router
from db.db import create_db_and_tables, SessionDep


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
