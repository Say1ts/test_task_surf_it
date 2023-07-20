from sqlalchemy.orm import Session

from ad.schema import AdGetQuery
from ad.services import handle_ads_sort
from db.connection import pg_db_session
from db.models import Ad, User, Review, Complain, Permission, Role
from db.schema import AdBase, ReviewBase, ComplainBase

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
    ad = session.query(Ad) \
        .filter(and_(
            Ad.id == ad_id,
            Ad.is_published)) \
        .first()
    print(ad_id)
    return ad


@pg_db_session
def delete_ad(ad_id: int, session=None) -> dict[str, str]:
    session.query(Ad) \
        .filter(Ad.id == ad_id) \
        .delete()
    session.commit()
    return {"message": "Ad deleted successfully"}


@pg_db_session
def edit_ad(ad_id: int, ad_data: AdBase, session=None):
    ad = session.query(Ad).filter(Ad.id == ad_id).first()
    if ad:
        for key, value in ad_data.dict().items():
            setattr(ad, key, value)
        session.commit()
        session.refresh(ad)
        return ad
    return None


@pg_db_session
def create_complain(complain_data: ComplainBase, session=None):
    new_complain = Complain(**complain_data.dict())
    session.add(new_complain)
    session.commit()
    session.refresh(new_complain)
    return new_complain


@pg_db_session
def list_complains(ad_id: int, session=None):
    return session.query(Complain).filter(Complain.ad_id == ad_id).all()


@pg_db_session
def create_review(review_data: ReviewBase, session=None):
    existing_review = session.query(Review)\
        .filter(
            Review.ad_id == review_data.ad_id,
            Review.created_by == review_data.created_by
        ).first()

    if existing_review:
        existing_review.score = review_data.score
        existing_review.content = review_data.content
        session.commit()
        session.refresh(existing_review)
        return existing_review

    new_review = Review(**review_data.dict())
    session.add(new_review)
    session.commit()
    session.refresh(new_review)
    return new_review


@pg_db_session
def list_reviews(ad_id: int, session=None):
    return session.query(Review).filter(Review.ad_id == ad_id).all()


@pg_db_session
def delete_review(review_id: int, session=None):
    review = session.query(Review).get(review_id)
    if review:
        session.delete(review)
        session.commit()
        return {"message": "Review deleted"}
    return {"message": "Review not found"}


@pg_db_session
def is_user_has_permission(
        user_id: int, permission_name: str, session=None) -> bool:
    """
    Check if a user has a specific permission based on their role.
    :return: True if the user has permission, False otherwise.
    """
    user = session.query(User).get(user_id)
    if not user:
        return False

    # Получить все разрешения, связанные с ролью пользователя.
    permissions = session.query(Permission).filter(
        and_(
            Permission.roles.any(Role.id == user.role_id),
            Permission.title == permission_name
        )
    ).all()
    return bool(permissions)
