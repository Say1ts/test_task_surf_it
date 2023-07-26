from configparser import ConfigParser
from typing import AsyncGenerator

import asyncpg
import sqlalchemy
from asyncpg import InterfaceError
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from log.logger import get_logger

config = ConfigParser()
config.read('./db/db_config.ini')
database_url = config.get('auth', 'database_url')
async_database_url = config.get('auth', 'async_database_url')


engine = create_async_engine(async_database_url)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            logger = get_logger()
            logger.critical(f'DataBase Error: {e}')
