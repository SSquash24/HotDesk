from datetime import date, timedelta

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pydantic import FilePath

from app import models, crud, schemas
from app.main import app, get_db
from app.dependencies import ADMIN_USER_SCHEMA, DUMMY_USER_SCHEMA
from app.schemas import BookingCreate, SeatCreate, PlanCreate


future_day = str(date.today()+timedelta(days=10))
tomorrow = str(date.today() + timedelta(days=1))

# create testing db and client ---------------------------


@pytest.fixture(scope="module")
def client():
    SQLALCHEMY_DATABASE_URL = "sqlite:///"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    models.Base.metadata.create_all(bind=engine)

            
    db = TestingSessionLocal()        
    crud.create_user(db, ADMIN_USER_SCHEMA)
    dummy_user = crud.create_user(db, DUMMY_USER_SCHEMA)
    db_plan = crud.create_plan(db, PlanCreate(name="testplan", path=FilePath("tests/testlayout.csv")))
    crud.create_seat(db, SeatCreate(
        name= "seat 0",
        x=0.0,
        y=0.0,
        plan_id=db_plan.id
    ))
    crud.create_booking(db, BookingCreate(date=tomorrow), dummy_user.id)
    db.close()

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)
    return client

@pytest.fixture(scope="module")
def admin_login(client):
    form_data = {
        "username": ADMIN_USER_SCHEMA.username,
        "password": ADMIN_USER_SCHEMA.password
    }

    response = client.post("/login", data=form_data, headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    return response


@pytest.fixture(scope="module")
def user_login(client):
    form_data = {
        "username": "Dummy",
        "password": "dummypassword"
    }

    response = client.post("/login", data=form_data, headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    return response

@pytest.fixture(scope="module")
def admin_token(admin_login):
    yield admin_login.json()['access_token']

@pytest.fixture(scope="module")
def user_token(user_login):
    yield user_login.json()['access_token']

@pytest.fixture(scope="module")
def single_booking(client, user_token):
    response = client.post("/bookings/book/", 
                           headers={"Authorization": f"Bearer {user_token}"}, 
                           json={"date": future_day})
    return response