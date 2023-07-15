from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/registration", tags=["Auth"])
async def registration_user():
    pass


@auth_router.post("/sign_in", tags=["Auth"])
async def sign_in_user():
    pass


@auth_router.post("/appoint_admin", tags=["Admin"])
async def appoint_admin():
    pass


@auth_router.post("/ban_user", tags=["Admin"])
async def ban_user():
    pass
