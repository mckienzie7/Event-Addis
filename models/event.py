# events.py (Ensure this is loaded first)
from sqlalchemy import Column, String, Integer, DateTime, Enum, ForeignKey, Table, TEXT
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
import base64

if models.storage_t == 'db':
    event_catagory = Table('event_catagory', Base.metadata,
                           Column('event_id', String(128),
                                  ForeignKey('events.id', onupdate='CASCADE', ondelete='CASCADE'),
                                  primary_key=True),
                           Column('catagory_id', String(128),
                                  ForeignKey('catagory.id', onupdate='CASCADE', ondelete='CASCADE'),
                                  primary_key=True))

from sqlalchemy import LargeBinary

class Events(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = 'events'

        place_id = Column(String(128), ForeignKey("place.id"), nullable=False)
        user_id = Column(String(128), ForeignKey("user.id"), nullable=False)
        title = Column(String(128), nullable=False)
        description = Column(String(128))
        Date = Column(DateTime, nullable=False)
        Address = Column(String(128))
        Banner = Column(LargeBinary)  # Use LargeBinary to store binary data
        status = Column(Enum('Active', 'Cancelled', 'Published'))
        catagories = relationship("Catagory", secondary=event_catagory, viewonly=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_dict(self):
        """Extend to_dict to include the full banner data as base64"""
        dictionary = super().to_dict()
        if self.Banner:
            dictionary['Banner'] = f"data:image/jpeg;base64,{base64.b64encode(self.Banner).decode('utf-8')}"
        return dictionary