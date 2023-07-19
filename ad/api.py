from ad import queries
from ad.queries import is_user_banned
from db.shema import AdBase


def create_ad(body: AdBase):
    if is_user_banned(body.owner):
        return
    return queries.create_ad(body)

