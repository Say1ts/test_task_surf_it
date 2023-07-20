from datetime import datetime
from fastapi import HTTPException

from ad import queries
from ad.queries import is_user_banned
from ad.schema import AdListQuery
from ad.services import handle_ads_filter
from db.schema import AdBase, ComplainBase, ReviewBase
from fastapi import HTTPException


def create_ad(body: AdBase):
    if is_user_banned(body.owner):
        return
    body.created_by = datetime.now()
    return queries.create_ad(body)


def list_ads(query: AdListQuery):
    start = (query.page - 1) * query.per_page
    end = start + query.per_page
    filter_conditions = handle_ads_filter(query)

    ads = queries.list_ads(filter_conditions, start, end, query.sort)
    return ads


def get_ad(ad_id: int):
    return queries.get_ad(ad_id)


def delete_ad(ad_id: int):
    return queries.delete_ad(ad_id)


def edit_ad(ad_id: int, current_user: int, ad_data: AdBase):
    ad = queries.get_ad(ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Ad not found")

    if current_user == ad.owner or queries.is_user_has_permission(current_user, "edit_ads"):
        return queries.edit_ad(ad_id, ad_data)

    raise HTTPException(status_code=403, detail="Not enough permissions")


def create_complain(complain: ComplainBase):
    if is_user_banned(complain.created_by):
        return
    complain.created_by = datetime.now()
    return queries.create_complain(complain)


def list_complains(ad_id: int):
    return queries.list_complains(ad_id)


def create_review(review: ReviewBase):
    if is_user_banned(review.created_by):
        return
    review.created_by = datetime.now()
    return queries.create_review(review)


def list_reviews(ad_id: int):
    return queries.list_reviews(ad_id)


def delete_review(review_id: int):
    return queries.delete_review(review_id)
