from ad.schema import AdGetQuery
from ad.services import handle_ads_sort
from db.connection import pg_db_session
from db.models import Ad, User
from db.schema import AdBase

from sqlalchemy import and_, Column


@pg_db_session
def create_ad(body: AdBase, session=None):
    new_ad = Ad(**body.dict())
    session.add(new_ad)
    session.commit()
    session.refresh(new_ad)
    return new_ad


@pg_db_session
def is_user_banned(user_id: int, session=None) -> bool:
    user = session.query(User.is_banned).filter(User.id == user_id).first()
    if user is None:
        return True
    return user.is_banned


@pg_db_session
def list_ads(
        filter_conditions: list[Column],
        start: int, end: int,
        sort: str = None, session=None):
    ads = session.query(Ad).filter(and_(*filter_conditions))
    ads = handle_ads_sort(ads, sort)
    ads = ads.slice(start, end).all()
    return ads


@pg_db_session
def get_ad(ad_id: int, session=None):
    ad = session.query(Ad)\
        .filter(and_(
            Ad.id == ad_id,
            Ad.is_published))\
        .first()
    return ad


@pg_db_session
def delete_ad(ad_id: int, session=None) -> str:
    session.query(Ad) \
        .filter(Ad.id == ad_id) \
        .delete()
    session.commit()
    return 'Ad deleted'
