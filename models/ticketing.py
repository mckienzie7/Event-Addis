#!/usr/bin/python3
"""
Ticketing class
"""
import enum

from sqlalchemy import Column, String,Enum, Float, Boolean
from os import getenv
import sqlalchemy
from sqlalchemy.orm import relationship
import models
from models.base_model import BaseModel, Base

class Ticketing(BaseModel, Base):
    """Representation of Ticketing"""

    if models.storage_t == 'db':
        __tablename__ = 'ticketing'

        ticket_type = Column(Enum("normal" , "VIP" , "VVIP"))
        price = Column(Float)
        refundable = Column(Boolean)


    
     

