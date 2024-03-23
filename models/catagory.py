#!/usr/bin/python3
"""
Catagory class
"""


from sqlalchemy import Column, String
import models
from models.base_model import BaseModel, Base


class Catagory(BaseModel, Base):
    """Representation of a Catagory"""
    if models.storage_t == 'db':
        __tablename__ = 'catagory'
        name = Column(String(128), nullable=False)
        discription = Column(String(128), nullable=True)

        

    def __init__(self, *args, **kwargs):
        """Intializes catagory"""
        super().__init__(*args, **kwargs)
