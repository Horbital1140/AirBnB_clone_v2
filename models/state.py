#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", back_populates="state", cascade="all, delete-orphan")

    @property
    def cities(self):
        """Returns a list of City instances with matching state_id."""
        from models import storage
        from models.city import City
        city_objs = storage.all(City)
        return [city for city in city_objs.values() if city.state_id == self.id]

    