from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ad import services
from ad.schema import AdListQuery
from db.connection import get_db
from db.schema import AdBase, ReviewBase, ComplainBase

ad_router = APIRouter(prefix="/ad")


@ad_router.post("/create", tags=["ad"])
async def create_ad(body: AdBase, db: AsyncSession = Depends(get_db)):
    return await services.create_ad(body, db)


@ad_router.post("/list", tags=["ad"])
async def list_ads(query: AdListQuery, db: AsyncSession = Depends(get_db)):
    return await services.list_ads(query, db)


@ad_router.get("/{ad_id}/get/", tags=["ad"])
async def get_ad(ad_id: int, db: AsyncSession = Depends(get_db)):
    return await services.get_ad(ad_id, db)


@ad_router.post("/ad_id}/edit", tags=["ad"])
async def edit_ad(ad_id: int, ad_data: AdBase, db: AsyncSession = Depends(get_db)):
    # current_user = get_current_user()
    current_user = 1
    return await services.edit_ad(ad_id, current_user, ad_data, db)


@ad_router.delete("/{ad_id}/delete/", tags=["ad"])
async def delete_ad(ad_id: int, db: AsyncSession = Depends(get_db)):
    return await services.delete_ad(ad_id, db)


@ad_router.post("/complains/create", tags=["ad_complains"])
async def complain_ad(complain: ComplainBase, db: AsyncSession = Depends(get_db)):
    return await services.create_complain(complain, db)


@ad_router.get("/complains/list/{ad_id}/", tags=["ad_complains"])
async def list_complains(ad_id: int, db: AsyncSession = Depends(get_db)):
    return await services.list_complains(ad_id, db)


@ad_router.post("/review/create/", tags=["ad_reviews"])
async def review_ad(review: ReviewBase, db: AsyncSession = Depends(get_db)):
    return await services.create_review(review, db)


@ad_router.get("/{ad_id}/review/list", tags=["ad_reviews"])
async def list_ad_reviews(ad_id: int, db: AsyncSession = Depends(get_db)):
    return await services.list_reviews(ad_id, db)


@ad_router.delete("/reviews/{review_id}", tags=["ad_reviews"])
async def delete_ad_review(review_id: int, db: AsyncSession = Depends(get_db)):
    return await services.delete_review(review_id, db)
