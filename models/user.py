#!/usr/bin/python3
"""
user class
"""
import enum

from sqlalchemy import Column, String, ForeignKey, Enum
from os import getenv
import sqlalchemy
from sqlalchemy.orm import relationship
from hashlib import md5
import models
from models.base_model import BaseModel, Base
class User(BaseModel, Base):
    """ Representation of User"""
    if models.storage_t == "db":
        __tablename__ = 'user'

        email = Column(String(128), nullable=False)
        fullname = Column(String(128), nullable=False)
        username = Column(String(128), nullable=False)

        password = Column(String(128), nullable=False)
        Role = Column(Enum("Attendee", "organizer","Adminstrator"))
        bio = Column(String(128))
        website = Column(String(128),)
        socialmedia = Column(String(128),)
        phone_number = Column(String(128), nullable=False)
        profile_picture = Column(String(128))
        events = relationship("Events",
                              backref="Organizer",
                              cascade="all, delete, delete-orphan")
        notification = relationship("Notification",
                                    backref="user",
                                    cascade="all, delete, delete-orphan")



    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)

