from sqlalchemy import Column, DECIMAL, DateTime, ForeignKey, func, Integer, String
from sqlalchemy.orm import relationship

from . import Base


class Ad(Base):
    __tablename__ = 'ad'

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)

    description = Column(String(1000), nullable=False)

    price = Column(DECIMAL, index=True)

    date = Column(DateTime, index=True, server_default=func.now())

    photos = relationship('Photo', back_populates='ad')


class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True, autoincrement=True)

    url = Column(String(512), nullable=False)

    ad_id = Column(Integer, ForeignKey('ad.id'))

    ad = relationship('Ad', back_populates='photos')
