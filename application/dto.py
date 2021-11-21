from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, conlist, constr, condecimal


class Message(BaseModel):
    detail: str


class Photo(BaseModel):
    url: HttpUrl

    class Config:
        orm_mode = True


class AdIn(BaseModel):
    name: constr(min_length=5, max_length=200)

    description: constr(min_length=10, max_length=1000)

    price: condecimal(ge=1.00, max_digits=9, decimal_places=2)

    photos: conlist(Photo, min_items=1, max_items=3)


class AdCreated(BaseModel):
    id: int


class AdShort(BaseModel):
    id: int

    name: str

    price: Decimal

    main_photo: Photo


class AdOut(BaseModel):
    id: int

    name: str

    description: Optional[str] = None

    price: Decimal

    photos: Optional[List[Photo]] = None

    main_photo: Photo

    class Config:
        orm_mode = True
    
    def dict(self, *args, **kwargs) -> str:
        kwargs['exclude_none'] = True
        return super().dict(*args, **kwargs)
    