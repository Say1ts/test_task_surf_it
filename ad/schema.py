from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CreationTimeInterval(BaseModel):
    older_then: Optional[datetime] = None
    newer_then: Optional[datetime] = None


class PriceInterval(BaseModel):
    price_gt: Optional[float] = None
    price_lt: Optional[float] = None


class AdListQuery(BaseModel):
    page: Optional[int] = Field(default=1, ge=1)
    per_page: Optional[int] = Field(default=10, ge=1, le=100)
    categories: Optional[List[int]] = None
    ad_type: Optional[int] = None
    sort: Optional[str] = None
    creation_time_interval: Optional[CreationTimeInterval] = None
    price_interval: Optional[PriceInterval] = None


class AdGetQuery(BaseModel):
    ad_id: int
