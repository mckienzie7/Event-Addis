#!/usr/bin/python3
"""
catagory class
"""
import enum

from sqlalchemy import Column, String
from os import getenv
import sqlalchemy
from sqlalchemy.orm import relationship
from hashlib import md5
import models
from models.base_model import BaseModel, Base


class Catagory(BaseModel, Base):
    """Representation of a Catagory"""
    if models.storage_t == 'db':
        __tablename__ = 'catagory'
        name = Column(String(128), nullable=False)
        discription = Column(String(128))
        

    def __init__(self, *args, **kwargs):
        """Intializes catagory"""
        super().__init__(*args, **kwargs)
