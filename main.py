from fastapi import FastAPI, Request
from fastapi.routing import APIRoute

from ad.routes import ad_router
from auth.auth import auth_backend, fastapi_users
from auth.schema import UserRead, UserCreate
from log.logger import get_logger


def custom_generate_unique_id(route: APIRoute):
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    generate_unique_id_function=custom_generate_unique_id,
    title="surf_it_test_task")

app.logger = get_logger()

app.include_router(ad_router)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
# @app.exception_handler(ValueError)
# async def value_error_exception_handler(request: Request, exc: ValueError):
#     return JSONResponse(
#         status_code=400,
#         content={"message": str(exc)},
#     )
#
#
# @app.exception_handler(500)
# async def internal_exception_handler(request: Request, exc: Exception):
#     return JSONResponse(status_code=500, content={"message": str(exc)})
