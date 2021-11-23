from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, condecimal, conlist, constr


class Message(BaseModel):
    detail: str = Field(..., example='NOT_FOUND')


class Photo(BaseModel):
    url: HttpUrl = Field(..., example='https://via.placeholder.com/1920x1080.png')

    class Config:
        orm_mode = True


class AdBase(BaseModel):
    name: constr(min_length=5, max_length=200) = Field(
        ..., example='Wireless Mouse'
    )

    price: condecimal(ge=1.00, max_digits=9, decimal_places=2) = Field(..., example=500)


class AdIn(AdBase):
    description: constr(min_length=10, max_length=1000) = Field(
        ..., example='2.4 GHz Wireless Cordless Mouse Mice Optical Scroll For PC Laptop Computer + USB'
    )

    photos: conlist(Photo, min_items=1, max_items=3)


class AdCreated(BaseModel):
    id: int = Field(..., title='Ad ID', example=1)

    class Config:
        orm_mode = True


class AdShort(AdCreated, AdBase):
    price: float = Field(..., example=500) # sqlite has some problems with decimals

    main_photo: Photo = Field(..., title='Main photo')

    class Config:
        orm_mode = True


class AdOut(AdShort):
    description: Optional[str] = Field(
        None, example='2.4 GHz Wireless Cordless Mouse Mice Optical Scroll For PC Laptop Computer + USB'
    )

    photos: Optional[List[Photo]] = None

    class Config:
        orm_mode = True
