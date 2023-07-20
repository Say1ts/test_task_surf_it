from ad import queries
from ad.queries import is_user_banned
from ad.schema import AdListQuery
from ad.services import handle_ads_filter
from db.schema import AdBase


def create_ad(body: AdBase):
    if is_user_banned(body.owner):
        return
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