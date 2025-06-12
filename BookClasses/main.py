import logging
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated
from datetime import datetime, timezone

from .database import engine, SessionLocal
from .models import Base, Classes, Booking
from pydantic import EmailStr
from .schemas import BookingCreate, ClassCreate
from fastapi.responses import JSONResponse

# Initialize logger
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()

# Create tables (in production use Alembic)
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get('/healthy', status_code=status.HTTP_200_OK)
def health_check():
    logger.info("Health check requested")
    return {'status': 'healthy'}

@app.post("/classes/", status_code=status.HTTP_201_CREATED)
async def create_class(class_data: ClassCreate, db: db_dependency):
    logger.info("Attempting to create class: %s", class_data.name)
    try:
        datetime_obj = datetime.fromisoformat(class_data.dateTime)
    except ValueError:
        logger.warning("Invalid datetime format received: %s", class_data.dateTime)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid datetime format. Please use ISO 8601 format (YYYY-MM-DDTHH:MM:SS)"
        )

    model = Classes(
        name=class_data.name,
        dateTime=datetime_obj,
        instructor=class_data.instructor,
        availableSlots=class_data.availableSlots
    )

    try:
        db.add(model)
        db.commit()
        db.refresh(model)
        logger.info("Class '%s' created successfully with ID %s", model.name, model.id)
        return {
            "message": "Class created successfully",
            "class_id": model.id,
            "class_details": {
                "name": model.name,
                "dateTime": model.dateTime.isoformat(),
                "instructor": model.instructor,
                "availableSlots": model.availableSlots
            }
        }
    except Exception as e:
        db.rollback()
        logger.error("Failed to create class: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/classesall", status_code=status.HTTP_200_OK)
async def read_classes(db: db_dependency):
    logger.info("Fetching all classes")
    classes = db.query(Classes).all()
    if not classes:
        logger.warning("No classes found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No classes found"
        )
    return classes

@app.get("/classes", status_code=status.HTTP_200_OK)
async def read_upcoming_classes(db: db_dependency):
    logger.info("Fetching upcoming classes")
    now_utc = datetime.now(timezone.utc)
    classes = db.query(Classes).filter(Classes.dateTime > now_utc).all()
    if not classes:
        logger.warning("No upcoming classes found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No classes found"
        )
    return classes

@app.post("/book", status_code=status.HTTP_201_CREATED)
async def book_class(booking: BookingCreate, db: db_dependency):
    logger.info("Attempting to book class ID %s for %s", booking.class_id, booking.client_email)
    fitness_class = db.query(Classes).filter(Classes.id == booking.class_id).first()
    if not fitness_class:
        logger.warning("Class with ID %s not found", booking.class_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    if fitness_class.availableSlots <= 0:
        logger.info("No available slots for class ID %s", booking.class_id)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No slots available"
        )

    new_booking = Booking(
        class_id=booking.class_id,
        client_name=booking.client_name,
        client_email=booking.client_email
    )

    fitness_class.availableSlots -= 1

    try:
        db.add(new_booking)
        db.commit()
        db.refresh(new_booking)
        logger.info("Booking successful for %s, booking ID %s", booking.client_email, new_booking.id)
        return {
            "message": "Booking successful",
            "booking_id": new_booking.id,
            "remaining_slots": fitness_class.availableSlots
        }
    except Exception as e:
        db.rollback()
        logger.error("Booking failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/bookings", status_code=status.HTTP_200_OK)
async def get_bookings_by_email(email: EmailStr, db: db_dependency):
    logger.info("Fetching bookings for email: %s", email)
    bookings = db.query(Booking).filter(Booking.client_email == email).all()
    if not bookings:
        logger.warning("No bookings found for email: %s", email)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No bookings found for this email"
        )
    return bookings
