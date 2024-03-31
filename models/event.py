#!/usr/bin/python3
"""
Event class
"""
import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table, DateTime, Enum
from os import getenv
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy.orm import relationship
import models
from models.catagory import Catagory
from models.place import Place
"""Associative Table event_catagory"""
if models.storage_t == 'db':
    event_catagory = Table('event_catagory', Base.metadata,
                           Column('event_id', String(128),
                                  ForeignKey('events.id', onupdate='CASCADE',
                                             ondelete='CASCADE'),
                                  primary_key=True),
                           Column('catagory_id', String(128),
                                  ForeignKey('catagory.id', onupdate='CASCADE',
                                             ondelete='CASCADE'),
                                  primary_key=True))

class Events(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = 'events'

        place_id = Column(String(128), ForeignKey("place.id"), nullable=False)
        user_id = Column(String(128), ForeignKey("user.id"), nullable=False)
        title = Column(String(128), nullable=False)
        description = Column(String(128))
        Date = Column(String(128), nullable=False)
        Address = Column(String(128))
        Banner = Column(String(128))
        status = Column(Enum('Active', 'Cancelled', 'Published'))
        catagories = relationship("Catagory",
                                  secondary=event_catagory,
                                  viewonly=False)


    def __init__(self, *args, **kwargs):
        """initializes Event"""
        super().__init__(*args, **kwargs)