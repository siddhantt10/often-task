# app/schemas.py
from typing import List, Optional
from pydantic import BaseModel

class AccommodationBase(BaseModel):
    name: str
    location: str

class TransferBase(BaseModel):
    mode: str
    from_location: str
    to_location: str

class ActivityBase(BaseModel):
    name: str
    description: Optional[str]

class DayBase(BaseModel):
    day_number: int
    date: Optional[str]
    accommodations: List[AccommodationBase] = []
    transfers: List[TransferBase] = []
    activities: List[ActivityBase] = []

class TripCreate(BaseModel):
    region: str
    name: str
    duration_nights: int
    days: List[DayBase]

class Accommodation(AccommodationBase):
    id: int
    class Config:
        orm_mode = True

class Transfer(TransferBase):
    id: int
    class Config:
        orm_mode = True

class Activity(ActivityBase):
    id: int
    class Config:
        orm_mode = True

class Day(DayBase):
    id: int
    accommodations: List[Accommodation] = []
    transfers: List[Transfer] = []
    activities: List[Activity] = []
    class Config:
        orm_mode = True

class Trip(TripCreate):
    id: int
    days: List[Day]
    class Config:
        orm_mode = True
