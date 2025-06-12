# Seed data is:

# Initial data to populate your database for testing, development, or demo purposes.

from BookClasses.database import SessionLocal
from BookClasses.models import Classes
from datetime import datetime

db = SessionLocal()

sample_classes = [
    Classes(
        name="Yoga Flow",
        dateTime=datetime.fromisoformat("2025-06-15T07:00:00"),
        instructor="Aarav Singh",
        availableSlots=15
    ),
    Classes(
        name="HIIT Blast",
        dateTime=datetime.fromisoformat("2025-06-15T09:00:00"),
        instructor="Riya Mehta",
        availableSlots=10
    )
]

db.add_all(sample_classes)
db.commit()
db.close()

print("Seed data added.")
