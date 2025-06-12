from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from .database import Base 

class Classes(Base):
    __tablename__ = "fitnessclasses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    dateTime = Column(DateTime, nullable=False)  # Matches ISO 8601
    instructor = Column(String, nullable=False)
    availableSlots = Column(Integer, nullable=False)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, nullable=False)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False)
