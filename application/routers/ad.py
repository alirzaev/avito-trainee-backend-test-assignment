from enum import Enum
from typing import List, Optional

from fastapi import APIRouter, Depends, Path, Query
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

from .. import crud
from ..crud import SortOrder
from ..database import get_db
from ..dto import AdCreated, AdIn, AdOut, AdShort, Message

router = APIRouter(prefix='/ad', tags=['ad'])


@router.get('/', response_model=List[AdShort], summary='Get a paginated list of ads')
def get_ads(
    date_order: Optional[SortOrder] = Query(None, title='Sort by date'),
    price_order: Optional[SortOrder] = Query(None, title='Sort by price'),
    page: Optional[int] = Query(1, ge=1, title='Page number. 10 items per page'),
    db: Session = Depends(get_db)
):    
    return [{
        'id': ad.id,
        'name': ad.name,
        'price': ad.price,
        'main_photo': ad.photos[0]
    } for ad in crud.get_ads(db, date_order, price_order, page)]


@router.post('/', status_code=201, response_model=AdCreated, summary='Create a new ad')
def add_ad(ad: AdIn, db: Session = Depends(get_db)):
    ad = crud.save_ad(db, ad)

    return ad


class ExtraFields(Enum):
    DESCRIPTION = 'description'
    PHOTOS = 'photos'


@router.get(
    '/{ad_id}',
    response_model=AdOut,
    response_model_exclude_none=True,
    summary='Get an ad by ID',
    responses={
        404: {'model': Message, 'description': 'Ad not found'}
    }
)
def get_ad_by_id(
    ad_id: int = Path(..., title="Ad ID"),
    fields: Optional[List[ExtraFields]] = Query([], title='Additional fields'),
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
