from fastapi import APIRouter

ad_router = APIRouter(prefix="/ad")


@ad_router.post("/create", tags=["ad"])
async def create_ad():
    pass


@ad_router.post("/list", tags=["ad"])
async def list_ad():
    pass


@ad_router.post("/{ad_id}/get/", tags=["ad"])
async def get_ad(ad_id: int):
    pass


@ad_router.post("/ad_id}/edit", tags=["ad"])
async def edit_ad():
    pass


@ad_router.post("/{ad_id}/delete/", tags=["ad"])
async def delete_ad(ad_id: int):
    pass


@ad_router.post("/{ad_id}/complain/create", tags=["ad_complains"])
async def complain_ad(ad_id: int):
    pass


@ad_router.post("/{ad_id}/complain/list", tags=["ad_complains"])
async def list_complains(ad_id: int):
    pass


@ad_router.post("/{ad_id}/review/create", tags=["ad_reviews"])
async def review_ad(ad_id: int):
    pass


@ad_router.post("/{ad_id}/review/delete", tags=["ad_reviews"])
async def delete_review_ad(ad_id: int):
    pass


