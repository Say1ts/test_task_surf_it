from db.connection import pg_db_session
from db.models import Ad, User
from db.shema import AdBase


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
