from enum import Enum
from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import asc, desc

from .database.models import Ad, Photo
from .dto import AdIn

PAGE_SIZE = 10


class SortOrder(str, Enum):
    ASC = 'asc'
    DESC = 'desc'


def get_ads(db: Session, date_order: SortOrder, price_order: SortOrder, page: int) -> List[Ad]:
    order = {
        SortOrder.ASC: asc,
        SortOrder.DESC: desc
    }

    return db.query(Ad) \
        .order_by(order[date_order](Ad.date)) \
        .order_by(order[price_order](Ad.price)) \
        .join(Photo) \
        .offset(PAGE_SIZE * (page - 1)) \
        .limit(PAGE_SIZE)


def get_ad_by_id(db: Session, id: int) -> Optional[Ad]:
    return db.query(Ad).get(id)


def save_ad(db: Session, ad: AdIn) -> int:
    ad_item = Ad(
        name=ad.name,
        description=ad.description,
        price=ad.price
    )
    db.add(ad_item)
    db.add_all([Photo(**photo.dict(), ad=ad_item) for photo in ad.photos])
    db.commit()
    db.refresh(ad_item)

    return ad_item.id
