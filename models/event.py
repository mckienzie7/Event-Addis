from sqlalchemy import Column, String, DateTime, Enum, ForeignKey, Table, LargeBinary
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import base64
import models

# Define association table for the many-to-many relationship between Events and Categories
if models.storage_t == 'db':
    event_catagory = Table('event_catagory', Base.metadata,
                           Column('event_id', String(128),
                                  ForeignKey('events.id', onupdate='CASCADE', ondelete='CASCADE'),
                                  primary_key=True),
                           Column('catagory_id', String(128),
                                  ForeignKey('catagory.id', onupdate='CASCADE', ondelete='CASCADE'),
                                  primary_key=True))

class Events(BaseModel, Base):
    """Event model to represent event data."""
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
        """Extend to_dict to include the full banner data as base64 and categories as a list of dictionaries."""
        dictionary = super().to_dict()
        if self.Banner:
            dictionary['Banner'] = f"data:image/jpeg;base64,{base64.b64encode(self.Banner).decode('utf-8')}"
        # Convert each category in 'catagories' to a dictionary
        dictionary['catagories'] = [cat.to_dict() for cat in self.catagories]
        return dictionary
