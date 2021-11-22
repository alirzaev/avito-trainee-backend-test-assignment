from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, conlist, constr, condecimal


class Message(BaseModel):
    detail: str = Field(..., example='NOT_FOUND')


class Photo(BaseModel):
    url: HttpUrl = Field(..., example='https://via.placeholder.com/1920x1080.png')

    class Config:
        orm_mode = True


class AdIn(BaseModel):
    name: constr(min_length=5, max_length=200)

    description: constr(min_length=10, max_length=1000)

    price: condecimal(ge=1.00, max_digits=9, decimal_places=2)

    photos: conlist(Photo, min_items=1, max_items=3)

    class Config:
        schema_extra = {
            'example': {
                'name': 'Wireless Mouse',
                'description': '2.4 GHz Wireless Cordless Mouse Mice Optical Scroll For PC Laptop Computer + USB',
                'price': '500',
                'photos': [
                    {
                        'url': 'https://via.placeholder.com/1920x1080.png?text=Mouse1'
                    },
                    {
                        'url': 'https://via.placeholder.com/1920x1080.png?text=Mouse2'
                    }
                ]
            }
        }


class AdCreated(BaseModel):
    id: int = Field(..., title='Ad ID', example=1)


class AdShort(BaseModel):
    id: int

    name: str

    price: Decimal

    main_photo: Photo = Field(..., title='Main photo')

    class Config:
        schema_extra = {
            'example': {
                'name': 'Wireless Mouse',
                'price': '500',
                'main_photo': {
                    'url': 'https://via.placeholder.com/1920x1080.png?text=Mouse1'
                }
            }
        }


class AdOut(BaseModel):
    id: int

    name: str

    description: Optional[str] = None

    price: Decimal

    photos: Optional[List[Photo]] = None

    main_photo: Photo = Field(..., title='Main photo')

    class Config:
        orm_mode = True

        schema_extra = {
            'example': {
                'name': 'Wireless Mouse',
                'description': '2.4 GHz Wireless Cordless Mouse Mice Optical Scroll For PC Laptop Computer + USB',
                'price': '500',
                'main_photo': {
                    'url': 'https://via.placeholder.com/1920x1080.png?text=Mouse1'
                },
                'photos': [
                    {
                        'url': 'https://via.placeholder.com/1920x1080.png?text=Mouse1'
                    },
                    {
                        'url': 'https://via.placeholder.com/1920x1080.png?text=Mouse2'
                    }
                ]
            }
        }
    
    def dict(self, *args, **kwargs) -> str:
        kwargs['exclude_none'] = True
        return super().dict(*args, **kwargs)
    