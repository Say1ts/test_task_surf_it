from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, Column, select, delete, update

from ad.filter_sort import handle_ads_sort
from db.models import Ad, User, Review, Complain, Permission, Role
from db.schema import AdBase, ReviewBase, ComplainBase, AdEdit


async def create_ad(body: AdBase, db: AsyncSession) -> Ad:
    new_ad = Ad(**body.dict())
    db.add(new_ad)
    await db.flush()
    await db.refresh(new_ad)
    return new_ad


async def is_user_banned(user_id: int, db: AsyncSession) -> bool:
    is_active = await db.execute(select(User.is_active).where(User.id == user_id))
    is_active = is_active.scalars().first()
    if is_active is None or not is_active:
        raise HTTPException(status_code=403, detail="Access is denied. The user is banned.")
    return False


async def list_ads(
        filter_conditions: list[Column],
        start: int, end: int, sort: str, db: AsyncSession):
    ads = select(Ad).where(and_(*filter_conditions))
    ads = handle_ads_sort(ads, sort)
    result = await db.execute(ads.slice(start, end))
    return result.scalars().all()


async def get_ad(ad_id: int, db: AsyncSession) -> Ad:
    stmt = select(Ad).where(and_(Ad.id == ad_id, Ad.is_published))
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def delete_ad(ad_id: int, db: AsyncSession) -> dict[str, str]:
    stmt = delete(Ad).where(Ad.id == ad_id)
    await db.execute(stmt)
    return {"message": "Ad deleted successfully"}


async def edit_ad(ad_id: int, ad_data: AdEdit, db: AsyncSession) -> Ad:
    stmt = update(Ad).where(Ad.id == ad_id).values(**ad_data.dict())
    await db.execute(stmt)
    return await get_ad(ad_id, db)


async def create_complain(complain_data: ComplainBase, db: AsyncSession) -> Complain:
    new_complain = Complain(**complain_data.dict())
    db.add(new_complain)
    await db.commit()
    await db.refresh(new_complain)
    return new_complain


async def list_complains(ad_id: int, db: AsyncSession):
    stmt = select(Complain).where(Complain.ad_id == ad_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_review(review_data: ReviewBase, db: AsyncSession) -> Review:
    stmt = select(Review).where(and_(Review.ad_id == review_data.ad_id, Review.created_by == review_data.created_by))
    result = await db.execute(stmt)
    existing_review = result.scalar_one_or_none()

    if existing_review:
        existing_review.score = review_data.score
        existing_review.content = review_data.content
        await db.commit()
        await db.refresh(existing_review)
        return existing_review

    new_review = Review(**review_data.dict())
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review


async def list_reviews(ad_id: int, db: AsyncSession):
    stmt = select(Review).where(Review.ad_id == ad_id)
    result = await db.execute(stmt)
    return result.scalars().all()


async def get_review(review_id: int, db: AsyncSession) -> Review:
    stmt = select(Review).where(Review.id == review_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def delete_review(review_id: int, db: AsyncSession) -> dict:
    stmt = delete(Review).where(Review.id == review_id)
    await db.execute(stmt)
    return {"message": "Review deleted"}


async def has_user_permission(user: User, permission_name: str, db: AsyncSession) -> bool:
    stmt = select(User).where(User.id == user.id)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        return False

    stmt = select(Permission).where(
        and_(Permission.roles.any(Role.id == user.role_id), Permission.title == permission_name))
    result = await db.execute(stmt)
    permissions = result.scalars().all()
    return bool(permissions)
