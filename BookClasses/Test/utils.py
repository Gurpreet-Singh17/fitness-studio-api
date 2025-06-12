from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app, get_db
from fastapi.testclient import TestClient
import pytest
from ..models import Booking, Classes


SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    return TestClient(app)

@pytest.fixture
def test_classes():
    db = TestingSessionLocal()
    test_class = Classes(
        name="Workout",
        dateTime=datetime.fromisoformat("2025-12-25T09:00:00"),
        instructor="Gurpreet",
        availableSlots=20
    )
    db.add(test_class)
    db.commit()
    db.refresh(test_class)
    yield test_class
    db.query(Classes).delete()
    db.commit()
    db.close()


@pytest.fixture
def test_booking(test_classes):
    db = TestingSessionLocal()
    test_booking = Booking(
        class_id=test_classes.id,
        client_name="Prince",
        client_email="prince@gmail.com"
    )
    db.add(test_booking)
    db.commit()
    yield test_booking
    db.query(Booking).delete()
    db.commit()
    db.close()
