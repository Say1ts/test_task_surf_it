from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


async def make_superuser(user_id: int, db: AsyncSession):
    user = select(User).where(User.id == user_id).values(
        is_superuser=True,
        role_id=2,
    )
    await db.execute(user)
    return user


async def ban_user(user_id: int, db: AsyncSession):
    user = select(User).where(User.id == user_id).values(
        is_active=False,
    )
    await db.execute(user)
    return user


async def unban_user(user_id: int, db: AsyncSession):
    user = select(User).where(User.id == user_id).values(
        is_active=True,
    )
    await db.execute(user)
    return user
