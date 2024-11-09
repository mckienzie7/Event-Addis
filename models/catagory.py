# catagory.py (Ensure this is loaded after Events)
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel, Base
import models

class Catagory(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = 'catagory'

        name = Column(String(128), nullable=False)
        discription = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)