from typing import Union
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String
from sqlmodel import SQLModel

from database import engine, create_all_tables
from controller import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield
    await engine.dispose()


app = FastAPI(lifespan=lifespan)

# Include the user router
app.include_router(users.router)
