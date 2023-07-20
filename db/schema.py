import datetime
from typing import List, Optional
from pydantic import BaseModel


class AdTypeBase(BaseModel):
    name: str


class AdType(AdTypeBase):
    """
    Type of ad:
        1: sale
        2: purchase
        3: service
    """
    id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    title: str


class Category(CategoryBase):
    id: int = None

    class Config:
        orm_mode = True


class AdBase(BaseModel):
    type_id: int = 1
    title: str = 'New ad'
    category_id: Optional[int] = None
    content: str
    is_published: bool = True
    owner: int
    price: Optional[float]
    created_at: datetime.datetime = datetime.datetime.now()


class Ad(AdBase):
    id: int
    ad_type: AdType
    category: Category

    class Config:
        orm_mode = True


class ComplainBase(BaseModel):
    ad_id: int
    title: str
    description: str
    created_by: int


class Complain(ComplainBase):
    id: int

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    ad_id: int
    score: int
    content: str
    created_by: int


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True


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


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    salt: str
    role_id: int
    is_banned: bool


class User(UserBase):
    id: int
    role: Role

    class Config:
        orm_mode = True

