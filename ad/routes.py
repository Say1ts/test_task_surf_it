from fastapi import APIRouter

from ad import api
from ad.schema import AdListQuery
from db.schema import AdBase, ReviewBase, ComplainBase

ad_router = APIRouter(prefix="/ad")


@ad_router.post("/create", tags=["ad"])
async def create_ad(body: AdBase):
    return api.create_ad(body)


@ad_router.post("/list", tags=["ad"])
async def list_ads(query: AdListQuery):
    return api.list_ads(query)


@ad_router.get("/{ad_id}/get/", tags=["ad"])
async def get_ad(ad_id: int):
    return api.get_ad(ad_id)


@ad_router.post("/ad_id}/edit", tags=["ad"])
async def edit_ad(ad_id, ad_data: AdBase):
    # current_user = get_current_user()
    current_user = 1
    return api.edit_ad(ad_id, current_user, ad_data)


@ad_router.delete("/{ad_id}/delete/", tags=["ad"])
async def delete_ad(ad_id: int):
    return api.delete_ad(ad_id)


@ad_router.post("/complains/create", tags=["ad_complains"])
async def complain_ad(complain: ComplainBase):
    return api.create_complain(complain)


@ad_router.get("/complains/list/{ad_id}/", tags=["ad_complains"])
async def list_complains(ad_id: int):
    return api.list_complains(ad_id)


@ad_router.post("/review/create/", tags=["ad_reviews"])
async def review_ad(review: ReviewBase):
    return api.create_review(review)


@ad_router.get("/{ad_id}/review/list", tags=["ad_reviews"])
async def list_ad_reviews(ad_id: int):
    return api.list_reviews(ad_id)


@ad_router.delete("/reviews/{review_id}", tags=["ad_reviews"])
async def delete_ad_review(review_id: int):
    return api.delete_review(review_id)
