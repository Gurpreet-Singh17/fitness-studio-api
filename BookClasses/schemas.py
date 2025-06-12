from pydantic import BaseModel, EmailStr


class ClassCreate(BaseModel):
    name: str
    dateTime: str  # This will be a string that we'll parse to datetime
    instructor: str
    availableSlots: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Yoga Morning",
                "dateTime": "2023-12-25T09:00:00",
                "instructor": "Jane Doe",
                "availableSlots": 20
            }
        }

class BookingCreate(BaseModel):
    class_id: int
    client_name: str
    client_email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "class_id": 1,
                "client_name": "Alice",
                "client_email": "alice@example.com"
            }
        }