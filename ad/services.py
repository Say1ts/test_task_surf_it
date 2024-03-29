from datetime import datetime

import sqlalchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ad import queries
from ad.schema import AdListQuery
from ad.filter_sort import handle_ads_filter
from db.models import User, Review
from db.schema import AdBase, ComplainBase, ReviewBase, AdEdit
from fastapi import HTTPException


def check_user_for_ban(user: User):
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Access is denied. The user is banned.")


async def create_ad(ad: AdBase, db: AsyncSession, user: User):
    check_user_for_ban(user)
    ad.owner = user.id
    ad.created_at = datetime.now()
    try:
        return await queries.create_ad(ad, db)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while creating the ad: {str(e)}")


async def list_ads(query: AdListQuery, db: AsyncSession):
    start = (query.page - 1) * query.per_page
    end = start + query.per_page
    filter_conditions = handle_ads_filter(query)

    ads = await queries.list_ads(filter_conditions, start, end, query.sort, db)
    return ads


async def get_ad(ad_id: int, db: AsyncSession):
    ad = await queries.get_ad(ad_id, db)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return ad


async def delete_ad(ad_id: int, db: AsyncSession, user: User):
    ad = await queries.get_ad(ad_id, db)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")

    if user.id == ad.owner or await queries.has_user_permission(user, "delete_ads", db):
        return await queries.delete_ad(ad_id, db)
    raise HTTPException(status_code=403, detail="Not enough permissions")


async def edit_ad(ad_id: int, user: User, ad_data: AdEdit, db: AsyncSession):
    check_user_for_ban(user)
    ad = await queries.get_ad(ad_id, db)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")

    if user.id == ad.owner or await queries.has_user_permission(user, "edit_ads", db):
        return await queries.edit_ad(ad_id, ad_data, db)

    raise HTTPException(status_code=403, detail="Not enough permissions")


async def create_complain(complain: ComplainBase, db: AsyncSession, user: User):
    check_user_for_ban(user)
    complain.created_at = datetime.now()
    complain.created_by = user.id
    try:
        return await queries.create_complain(complain, db)
    except sqlalchemy.exc.IntegrityError:
        raise HTTPException(status_code=404, detail="Ad not found")


async def list_complains(ad_id: int, db: AsyncSession):
    ad = await queries.get_ad(ad_id, db)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return await queries.list_complains(ad_id, db)


async def create_review(review: ReviewBase, db: AsyncSession, user: User):
    check_user_for_ban(user)
    review.created_at = datetime.now()
    review.created_by = user.id
    return await queries.create_review(review, db)


async def list_reviews(ad_id: int, db: AsyncSession):
    ad = await queries.get_ad(ad_id, db)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")
    return await queries.list_reviews(ad_id, db)


async def delete_review(review_id: int, db: AsyncSession, user: User):
    check_user_for_ban(user)
    review: Review = await queries.get_review(review_id, db)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    if user.id == review.created_by or await queries.has_user_permission(user, "delete_review", db):
        return await queries.delete_review(review_id, db)

    raise HTTPException(status_code=403, detail="Not enough permissions")
