#!/usr/bin/python3
"""This module defines the Amenity class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.place import place_amenity


class Amenity(BaseModel, Base):
    """Amenity class to store amenities information"""
    __tablename__ = 'amenities'
    name = Column(String(128), nullable=False)

    # Relationship with Place for Many-To-Many
    place_amenities = relationship("Place", secondary=place_amenity, back_populates="amenities")
