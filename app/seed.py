# app/seed.py
from app.database import SessionLocal, engine, Base
from app.models import Trip, Day, Accommodation, Transfer, Activity

# Recreate all tables
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    try:
        regions = ["Phuket", "Krabi"]
        hotel_names = {
            "Phuket": [
                "Katathani Phuket Beach Resort",
                "Outrigger Laguna Phuket Beach Resort",
                "The Slate Phuket"
            ],
            "Krabi": [
                "Rayavadee",
                "Centara Grand Beach Resort & Villas Krabi",
                "Railay Beach Resort & Spa"
            ]
        }
        activities_pool = {
            "Phuket": [
                "Beach Day at Kata Noi",
                "Phi Phi Islands Tour",
                "Big Buddha Visit",
                "Old Phuket Town Walk"
            ],
            "Krabi": [
                "Railay Beach Climbing",
                "Emerald Pool Visit",
                "Island Hopping Tour",
                "Tiger Cave Temple Climb"
            ]
        }

        for region in regions:
            for nights in range(2, 9):  # 2 to 8 nights
                trip = Trip(
                    region=region,
                    name=f"{nights}-Night {region} Adventure",
                    duration_nights=nights
                )
                db.add(trip)
                db.flush()  # get trip.id

                for day_num in range(1, nights + 1):
                    day = Day(
                        trip_id=trip.id,
                        day_number=day_num,
                        date=None
                    )
                    db.add(day)
                    db.flush()

                    # Accommodation
                    hotel = hotel_names[region][(day_num - 1) % len(hotel_names[region])]
                    db.add(
                        Accommodation(
                            day_id=day.id,
                            name=hotel,
                            location=region
                        )
                    )

                    # Transfer
                    mode = "Taxi" if day_num == 1 else "Ferry"
                    from_loc = f"{region} Airport" if day_num == 1 else f"{region} Island Dock"
                    to_loc = hotel
                    db.add(
                        Transfer(
                            day_id=day.id,
                            mode=mode,
                            from_location=from_loc,
                            to_location=to_loc
                        )
                    )

                    # Activity
                    activity = activities_pool[region][(day_num - 1) % len(activities_pool[region])]
                    db.add(
                        Activity(
                            day_id=day.id,
                            name=activity,
                            description=f"Enjoy a {activity.lower()}"
                        )
                    )

                db.commit()
        print("Seed data inserted successfully.")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()