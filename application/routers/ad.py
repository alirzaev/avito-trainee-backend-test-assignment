from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..crud import SortOrder
from ..database import get_db
from ..dto import AdCreated, AdIn, AdOut, AdShort, Message

router = APIRouter(prefix='/ad')


@router.get('/', response_model=List[AdShort])
def get_ads(
    date_order: Optional[SortOrder] = SortOrder.DESC,
    price_order: Optional[SortOrder] = SortOrder.DESC,
    page: Optional[int] = Query(1, ge=1),
    db: Session = Depends(get_db)
):    
    return [{
        'id': ad.id,
        'name': ad.name,
        'price': ad.price,
        'main_photo': ad.photos[0]
    } for ad in crud.get_ads(db, date_order, price_order, page)]


@router.post('/', status_code=201, response_model=AdCreated)
def add_ad(ad: AdIn, db: Session = Depends(get_db)):
    ad_id = crud.save_ad(db, ad)

    return AdCreated(id=ad_id)


class ExtraFields(Enum):
    DESCRIPTION = 'description'
    PHOTOS = 'photos'


@router.get('/{ad_id}', response_model=AdOut, responses={
    404: {'model': Message, 'description': 'Ad not found'}
})
def get_ad_by_id(
    ad_id: int,
    fields: Optional[List[ExtraFields]] = Query([]),
    db: Session = Depends(get_db)
):
    ad = crud.get_ad_by_id(db, ad_id)

    if ad is None:
        raise HTTPException(status_code=404, detail='NOT_FOUND')
    
    data = {
        'id': ad.id,
        'name': ad.name,
        'price': ad.price,
        'main_photo': ad.photos[0]
    }

    if ExtraFields.DESCRIPTION in fields:
        data['description'] = ad.description
    if ExtraFields.PHOTOS in fields:
        data['photos'] = ad.photos
    
    return data
