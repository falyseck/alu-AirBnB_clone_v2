#!/usr/bin/python3
"""This module defines the Place class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

# Many-to-Many relationship table
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """A place to stay"""
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    # Relationship with Review for DBStorage
    reviews = relationship("Review", backref="place", cascade="all, delete")

    # Relationship with Amenity for DBStorage
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="place_amenities", viewonly=False)

    # Getter and Setter for amenities (FileStorage)
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def amenities(self):
            """Getter for amenities when using FileStorage"""
            from models import storage
            all_amenities = storage.all(Amenity)
            return [amenity for amenity in all_amenities.values() if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter for amenities when using FileStorage"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)
