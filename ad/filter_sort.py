from sqlalchemy import desc, Column

from ad.schema import AdListQuery
from db.models import Ad


def handle_ads_filter(query: AdListQuery) -> list[Column]:
    """
    Handle filtering for ads
    """

    filter_conditions = [Ad.is_published]

    if query.categories:
        filter_conditions.append(Ad.category_id.in_(query.categories))

    if query.ad_type:
        filter_conditions.append(Ad.type_id == query.ad_type)

    # Filter time intervals of creating ads
    if query.creation_time_interval:
        if query.creation_time_interval.newer_then:
            naive_datetime = query.creation_time_interval.newer_then.replace(tzinfo=None)
            filter_conditions.append(Ad.created_at >= naive_datetime)
        if query.creation_time_interval.older_then:
            naive_datetime = query.creation_time_interval.older_then.replace(tzinfo=None)
            filter_conditions.append(Ad.created_at <= naive_datetime)

    # Filter price intervals of creating ads
    if query.price_interval:
        if query.price_interval.price_gt:
            filter_conditions.append(Ad.price >= query.price_interval.price_gt)
        if query.price_interval.price_lt:
            filter_conditions.append(Ad.price <= query.price_interval.price_lt)

    return filter_conditions


def handle_ads_sort(ads, sort):
    if sort:
        if sort == 'created_at':
            ads = ads.order_by(Ad.created_at)
        elif sort == '-created_at':
            ads.order_by(desc(Ad.created_at))
        elif sort == 'price':
            ads = ads.order_by(Ad.price)
        elif sort == '-price':
            ads = ads.order_by(desc(Ad.price))
    return ads
