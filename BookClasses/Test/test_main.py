from datetime import datetime
from fastapi import status
from ..models import Classes, Booking
from .utils import client, test_classes, test_booking, TestingSessionLocal
import pytest


def test_health_check(client):
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'healthy'}


def test_read_classes(client, test_classes):
    response = client.get("/classesall")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'name': 'Workout',
        'dateTime': '2025-12-25T09:00:00',
        'instructor': 'Gurpreet',
        'availableSlots': 20,
        'id': test_classes.id
    }]


def test_read_upcoming_classes(client, test_classes):
    response = client.get("/classes")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'name': 'Workout',
        'dateTime': '2025-12-25T09:00:00',
        'instructor': 'Gurpreet',
        'availableSlots': 20,
        'id': test_classes.id
    }]


def test_create_valid_class(client):
    request_data = {
        'name': 'Yoga',
        'dateTime': '2025-12-30T08:00:00',
        'instructor': 'Shivam',
        'availableSlots': 15
    }

    response = client.post('/classes/', json=request_data)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    model = db.query(Classes).filter(Classes.name == 'Yoga').first()
    assert model is not None
    assert model.instructor == 'Shivam'
    assert model.availableSlots == 15
    assert model.dateTime == datetime(2025, 12, 30, 8, 0)
    db.close()


def test_create_class_invalid_datetime(client):
    bad_request = {
        'name': 'Bad Class',
        'dateTime': '25-12-2025 09:00',  # wrong format
        'instructor': 'Test',
        'availableSlots': 10
    }
    response = client.post('/classes/', json=bad_request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_class_missing_field(client):
    incomplete_request = {
        'name': 'Incomplete Class',
        'instructor': 'InstructorX',
        'availableSlots': 5
    }
    response = client.post('/classes/', json=incomplete_request)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_book_valid(client, test_classes):
    request_body = {
        'class_id': test_classes.id,
        'client_name': 'Gurpreet',
        'client_email': 'gur@gmail.com'
    }

    response = client.post('/book', json=request_body)
    assert response.status_code == status.HTTP_201_CREATED

    db = TestingSessionLocal()
    booking = db.query(Booking).filter(Booking.class_id == test_classes.id).first()
    assert booking is not None
    assert booking.client_name == 'Gurpreet'
    assert booking.client_email == 'gur@gmail.com'
    db.close()


def test_book_nonexistent_class(client):
    request_body = {
        'class_id': 999,  # ID that doesn't exist
        'client_name': 'Ghost',
        'client_email': 'ghost@example.com'
    }
    response = client.post('/book', json=request_body)
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_book_class_no_slots(client):
    db = TestingSessionLocal()
    # Create a class with 0 slots
    no_slot_class = Classes(
        name='Full Class',
        dateTime=datetime(2025, 12, 31, 10, 0),
        instructor='Max',
        availableSlots=0
    )
    db.add(no_slot_class)
    db.commit()
    db.refresh(no_slot_class)
    db.close()

    request_body = {
        'class_id': no_slot_class.id,
        'client_name': 'TestUser',
        'client_email': 'testuser@example.com'
    }
    response = client.post('/book', json=request_body)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_bookings_by_email(client, test_booking):
    response = client.get('/bookings', params={'email': 'prince@gmail.com'})
    assert response.status_code == status.HTTP_200_OK

    expected_data = [{
        "id": test_booking.id,
        "class_id": test_booking.class_id,
        "client_name": "Prince",
        "client_email": "prince@gmail.com"
    }]
    assert response.json() == expected_data


def test_bookings_email_not_found(client):
    response = client.get('/bookings', params={'email': 'notfound@example.com'})
    assert response.status_code == status.HTTP_404_NOT_FOUND
