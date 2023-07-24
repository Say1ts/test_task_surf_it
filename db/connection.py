from configparser import ConfigParser
from functools import wraps

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette import status

config = ConfigParser()
config.read('./db/db_config.ini')
database_url = config.get('auth', 'database_url')
async_database_url = config.get('auth', 'async_database_url')


engine = create_async_engine(async_database_url)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db():
    async with async_session() as session:
        yield session
        await session.commit()
        # try:
        #     yield session
        #     await session.commit()
        # except Exception as e:
        #     await session.rollback()
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail=str(e),
        #     )
