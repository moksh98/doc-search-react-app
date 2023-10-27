from fastapi import Depends
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from functools import lru_cache
from app.models import collections
from app.core.settings import settings


DATABASE_URL = "postgresql+asyncpg://"+settings.DB_USER+":"+settings.DB_PASS+"@"+settings.DB_URL+":"+str(settings.DB_PORT)+"/"+settings.DATABASE

engine = create_async_engine(DATABASE_URL,echo=True)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

### DO NOT CALL THIS FUNCTION UNLESS YOU'RE RESETTING THE DATABASE
async def create_db_and_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(user.Base.metadata.create_all)
        await conn.run_sync(collections.Base.metadata.create_all)

async def get_async_session():
    async with async_session_maker() as session:
        return session

