#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
import models
import os


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':

        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)

        # Define the relationship with State
        state = relationship("State", cascade='all, delete',
                             back_populates="cities")

        # Define the relationship with Place
        places = relationship("Place", cascade='all, delete', backref="cities")

    else:
        name = ""
        state_id = ""
