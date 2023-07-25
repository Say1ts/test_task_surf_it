from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel
from pydantic.version import VERSION as PYDANTIC_VERSION

PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")


class RoleBase(BaseModel):
    role_name: str
    description: str


class Role(RoleBase):
    id: int

    class Config:
        orm_mode = True


class PermissionBase(BaseModel):
    title: str
    description: str


class Permission(PermissionBase):
    id: int

    class Config:
        orm_mode = True


class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    username: str
    first_name: str
    last_name: str
    role_id: int

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False

    username: str
    first_name: str
    last_name: str
    role_id: int


class UserUpdate(schemas.BaseUserUpdate):
    pass
