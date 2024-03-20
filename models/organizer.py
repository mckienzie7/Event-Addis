#!/usr/bin/python3
"""
Organizer class
"""
import enum

from sqlalchemy import Column, String
from os import getenv
import sqlalchemy
from sqlalchemy.orm import relationship
from hashlib import md5
import models
from models.user import User
from models.base_model import BaseModel, Base

class Organizer(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = 'organizer'
        bio = Column(String(128), nullable=False)
        website = Column(String(128), nullable=False)
        socialmedia = Column(String(128), nullable=False)
        phone_number = Column(String(128), nullable=False)
        



    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)