from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

import auth.queries as queries
from auth.auth import fastapi_users
from db.connection import get_db
from db.models import User

auth_router = APIRouter(prefix="/auth")
current_superuser = fastapi_users.current_user(active=True, superuser=True)


@auth_router.post("/make_superuser", tags=["Admin"])
async def make_superuser(
        user_to_admin: int, db: AsyncSession = Depends(get_db), user: User = Depends(current_superuser)):
    return await queries.make_superuser(user_to_admin, db)


@auth_router.post("/ban_user", tags=["Admin"])
async def ban_user(
        user_to_ban: int, db: AsyncSession = Depends(get_db), user: User = Depends(current_superuser)):
    return await queries.ban_user(user_to_ban, db)


@auth_router.post("/unban_user", tags=["Admin"])
async def unban_user(
        user_to_ban: int, db: AsyncSession = Depends(get_db), user: User = Depends(current_superuser)):
    return await queries.ban_user(user_to_ban, db)
