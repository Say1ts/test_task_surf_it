from fastapi_users import FastAPIUsers
from fastapi_users.authentication import BearerTransport, CookieTransport, JWTStrategy, AuthenticationBackend

from .manager import get_user_manager
from db.models import User

# import os
# SECRET = os.getenv("SECRET")
# bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

SECRET = "5IUx93D1&YaouLO&SYtGT_AUcsBBvB0N"

cookie_transport = CookieTransport(
    cookie_name='ads_surf_it',
    cookie_max_age=3600,
    cookie_secure=True,
)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=SECRET,
        lifetime_seconds=86400,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
