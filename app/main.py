from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from .database import SessionLocal, engine, Base
from fastapi import FastAPI
from typing import List

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()      
    try:
        yield db
    finally:
        db.close()


# endpoints

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/itineraries/", response_model=schemas.Trip, status_code=status.HTTP_201_CREATED)
def create_itinerary(trip_in: schemas.TripCreate, db: Session = Depends(get_db)):
    # 1) Create Trip
    trip = models.Trip(
        region=trip_in.region,
        name=trip_in.name,
        duration_nights=trip_in.duration_nights
    )
    db.add(trip)
    db.flush()  # get trip.id

    # 2) Create Days & Nested
    for day_in in trip_in.days:
        day = models.Day(
            trip_id=trip.id,
            day_number=day_in.day_number,
            date=day_in.date
        )
        db.add(day)
        db.flush()
        # nested accommodations/transfers/activities
        for acc in day_in.accommodations:
            db.add(models.Accommodation(day_id=day.id, **acc.model_dump()))
        for tr in day_in.transfers:
            db.add(models.Transfer(day_id=day.id, **tr.model_dump()))
        for act in day_in.activities:
            db.add(models.Activity(day_id=day.id, **act.model_dump()))

    db.commit()
    db.refresh(trip)
    return trip

@app.get("/itineraries/", response_model=List[schemas.Trip])
def list_itineraries(db: Session = Depends(get_db)):
    return db.query(models.Trip).all()

@app.get("/itineraries/{trip_id}", response_model=schemas.Trip)
def get_itinerary(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(models.Trip).filter(models.Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Itinerary not found")
    return trip

@app.get("/recommended/", response_model=List[schemas.Trip])
def recommend(nights: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Trip)
          .filter(models.Trip.duration_nights == nights)
          .order_by(models.Trip.id)  # or popularity
          .all()
    )