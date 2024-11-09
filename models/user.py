#!/usr/bin/python3
"""
user class
"""
import enum
from models.base_model import BaseModel, Base
from sqlalchemy import Column, LargeBinary, String, Integer, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from hashlib import md5
import models
import bcrypt

from datetime import datetime, timedelta

class User(BaseModel, Base):
    """ Representation of User"""
    if models.storage_t == "db":
        __tablename__ = 'user'
        


        username = Column(String(80), unique=True, nullable=False)
        email = Column(String(120), unique=True, nullable=False)
        password = Column(String(255), nullable=False)
        bio = Column(Text)
        admin = Column(Boolean,nullable=True ,default=False)
        is_organizer = Column(Boolean, default=False)
        session_id = Column(String(250))
        reset_token = Column(String(250))
        gender = Column(String(10))
        age = Column(Integer)
        interests = Column(String(255))
        location = Column(String(100))
        hobbies = Column(String(255))
        preferences = Column(String(255))
        is_verified = Column(Boolean, default=False)
        created_at = Column(String(100))
        updated_at = Column(String(100))
        socialmedia = Column(String(128),)
        phone_number = Column(String(128))
        profile_picture = Column(String(128))
        session_expiration = Column(DateTime, nullable=True)
        events = relationship("Events",
                              backref="Organizer",
                              cascade="all, delete, delete-orphan")
        notification = relationship("Notification",
                                    backref="user",
                                    cascade="all, delete, delete-orphan")



    def set_password(self, password):
        """Hash the password for security"""
        self.password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password):
        """Check the provided password against the stored hash"""
        return self.password == md5(password.encode()).hexdigest()

