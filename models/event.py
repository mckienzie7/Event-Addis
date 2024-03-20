#!/usr/bin/python3
"""
Event class
"""
import enum
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table, DateTime
from os import getenv
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy.orm import relationship
import models

"""Associative Table event_catagory"""
if models.storage_t == 'db':
    event_catagory = Table('event_catagory', Base.metadata,
                           Column('event_id', String(128),
                           ForeignKey('event.id', onupdate='CASCADE',
                                                    ondelete='CASCADE'),
                                                primary_key=True),
                           Column('catagory_id', String(128),
                                        ForeignKey('catagory.id', onupdate='CASCADE',
                                                                        ondelete='CASCADE'),
                                                    primary_key=True))

class Events(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = 'events'

        organizer_id = Column(String(128), ForeignKey('catagory'), nullable=False)
        title = Column(String(128), nullable=False)
        description = Column(String(128))
        Date = Column(DateTime)
        Address = Column(String(128))
        Banner = Column(String(128), nullable=False)
        status = enum.Enum('status', ['Active', 'Cancelled', 'Published'])
        catagories = relationship("Catagory",
                                            secondary=event_catagory,
                                            viewonly=False)
        places = relationship("Place",
                                backref="events",
                                    cascade="all, delete, delete-orphan")



    def __init__(self, *args, **kwargs):
        """initializes Event"""
        super().__init__(*args, **kwargs)