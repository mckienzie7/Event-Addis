#!/usr/bin/python3
"""
user class
"""
import enum

from sqlalchemy import Column, String
from os import getenv
import sqlalchemy
from sqlalchemy.orm import relationship
from models.user import User
import models
from models.base_model import BaseModel, Base

class Attendee(BaseModel, User, Base):
    if models.storage_t == 'db':
        __tablename__ = 'attendee'
        
