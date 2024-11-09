from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models

class Place(BaseModel, Base):
    """Representation of Place"""
    if models.storage_t == 'db':  # This ensures the model is only used when working with the database
        __tablename__ = "place"

        name = Column(String(128), nullable=False)
        address = Column(String(128), nullable=False)
        capacities = Column(String(128))
        phone_number = Column(String(128))
        facilities = Column(String(128))

        events = relationship("Events", backref="places", cascade="all, delete, delete-orphan")
