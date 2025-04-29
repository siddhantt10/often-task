from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from .database import Base

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    region = Column(String, nullable=False, index=True)          # e.g. "Phuket"
    name = Column(String, nullable=False)                        # descriptive title
    duration_nights = Column(Integer, nullable=False, index=True)

    # relationships
    days = relationship("Day", back_populates="trip", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_trips_region_duration', 'region', 'duration_nights'),
    )

class Day(Base):
    __tablename__ = "days"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id", ondelete="CASCADE"), nullable=False)
    day_number = Column(Integer, nullable=False)  # 1-based day index
    date = Column(String, nullable=True)

    trip = relationship("Trip", back_populates="days")
    accommodations = relationship("Accommodation", back_populates="day", cascade="all, delete-orphan")
    transfers = relationship("Transfer", back_populates="day", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="day", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_days_trip_day', 'trip_id', 'day_number', unique=True),
    )

class Accommodation(Base):
    __tablename__ = "accommodations"
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

    day = relationship("Day", back_populates="accommodations")

class Transfer(Base):
    __tablename__ = "transfers"
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    mode = Column(String, nullable=False)         # e.g. Taxi, Ferry
    from_location = Column(String, nullable=False)
    to_location = Column(String, nullable=False)

    day = relationship("Day", back_populates="transfers")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("days.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    day = relationship("Day", back_populates="activities")