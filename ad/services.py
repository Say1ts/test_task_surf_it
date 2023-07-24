from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from ad import queries
from ad.queries import is_user_banned
from ad.schema import AdListQuery
from ad.filter_sort import handle_ads_filter
from db.schema import AdBase, ComplainBase, ReviewBase
from fastapi import HTTPException


async def create_ad(body: AdBase, db: AsyncSession):
    if await is_user_banned(body.owner, db):
        return
    body.created_at = datetime.now()
    return await queries.create_ad(body, db)


async def list_ads(query: AdListQuery, db: AsyncSession):
    start = (query.page - 1) * query.per_page
    end = start + query.per_page
    filter_conditions = handle_ads_filter(query)

    ads = await queries.list_ads(filter_conditions, start, end, query.sort, db)
    return ads


async def get_ad(ad_id: int, db: AsyncSession):
    return await queries.get_ad(ad_id, db)


async def delete_ad(ad_id: int, db: AsyncSession):
    return await queries.delete_ad(ad_id, db)


async def edit_ad(ad_id: int, current_user: int, ad_data: AdBase, db: AsyncSession):
    ad = await queries.get_ad(ad_id, db)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")

    if current_user == ad.owner or await queries.is_user_has_permission(current_user, "edit_ads"):
        return await queries.edit_ad(ad_id, ad_data, db)

    raise HTTPException(status_code=403, detail="Not enough permissions")


async def create_complain(complain: ComplainBase, db: AsyncSession):
    if await is_user_banned(complain.created_by, db):
        return
    complain.created_at = datetime.now()
    return await queries.create_complain(complain, db)


async def list_complains(ad_id: int, db: AsyncSession):
    return await queries.list_complains(ad_id, db)


async def create_review(review: ReviewBase, db: AsyncSession):
    if await is_user_banned(review.created_by, db):
        return
    review.created_at = datetime.now()
    return await queries.create_review(review, db)


async def list_reviews(ad_id: int, db: AsyncSession):
    return await queries.list_reviews(ad_id, db)


async def delete_review(review_id: int, db: AsyncSession):
    return await queries.delete_review(review_id, db)
