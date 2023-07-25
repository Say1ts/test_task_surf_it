import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


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
    created_at: datetime.datetime = None


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
    created_at: datetime.datetime = None


class Complain(ComplainBase):
    id: int

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    ad_id: int
    score: int = Field(ge=1, le=10)
    content: str
    created_by: int
    created_at: datetime.datetime = None


class Review(ReviewBase):
    id: int

    class Config:
        orm_mode = True


