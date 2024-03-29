#!/usr/bin/python3
"""
Ticketing class
"""
import enum

from sqlalchemy import Column, String
from os import getenv
import sqlalchemy
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base

class Ticketing(BaseModel, Base):
    """Representation of Ticketing"""

    if models.storage_t == 'db':
        __tablename__ = 'ticketing'

