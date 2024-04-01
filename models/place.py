#!/usr/bin/python
""" holds class Place"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table, ARRAY
from sqlalchemy.orm import relationship



class Place(BaseModel, Base):
    """Representation of Place"""
    if models.storage_t == 'db':
        __tablename__ = "place"

        name = Column(String(128), nullable=False)
        address = Column(String(128), nullable=False)
        capacities = Column(String(128))
        phone_number = Column(String(128), nullable=False)
        facilities = Column(String(128))

        events = relationship("Events",
                              backref="places",
                              cascade="all, delete, delete-orphan")


    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)
