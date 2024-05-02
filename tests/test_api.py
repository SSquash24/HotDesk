from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# from ..app.database import Base
from app import models, crud
from app.main import app, get_db
from app.routers.admin import ADMIN_USER_SCHEMA
from app.dependencies import ContextManager

from datetime import date, timedelta

# create testing db and client ---------------------------

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
models.Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()



app.dependency_overrides[get_db] = override_get_db



client = TestClient(app)

with ContextManager() as db:
    crud.create_user(db, ADMIN_USER_SCHEMA)

# Login -------------------------------------------------------------

def test_login():
    form_data = {
        "username": "Admin",
        "password": "admin"
    }

    response = client.post("/login", data=form_data, headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    assert response.status_code == 200
    return "bearer " + response.json()['access_token']


def test_login_bad_user():
    form_data = {
        "username": "fake guy 123",
        "password": "psswd"
    }

    response = client.post("/login", data=form_data, headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Incorrect username or password"
    }




# USER CALLS ------------------------------------------------------------------

def test_user_me_bad_token():
    response = client.get("/users/me", headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_user_me_():
    token = test_login()
    response = client.get("/users/me", headers={"Authorization": token})
    assert response.status_code == 200

    json = response.json()
    assert json['username'] == 'Admin'
    assert json['department'] == None
    assert json['role'] == 'admin'


def test_user_password_bad_token():
    response = client.get("/users/password?password=dummypw", headers={"Authorization": "a bad one!"})
    assert response.status_code == 405
    assert response.json() == {
        "detail": "Method Not Allowed"
    }

def test_user_password():
    token = test_login()
    response = client.post("/users/password?password=dummypw", headers={"Authorization": token})
    assert response.status_code == 200


# BOOKINGS CALLS ------------------------------------------------------------

tomorrow = str(date.today() + timedelta(1))


def test_bookings_book_bad_token():
    response = client.post("/bookings/book/", headers={"Authorization": "a bad one!"}, json={
        "date": tomorrow
    })
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_book():
    token = test_login()
    response = client.get("/bookings/book/", headers={"Authorization": token}, json={
        "date": tomorrow
    })
    assert response.status_code == 200
    assert response.json()['date'] == tomorrow


def test_bookings_me_bad_token():
    response = client.get("/bookings/me", headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_me():
    pass # TODO


def test_bookings_date_bad_token():
    response = client.get(f"/bookings/date?date={tomorrow}", headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_date():
    pass # TODO




# ADMIN CALLS -----------------------------------------------------------

def test_admin_user_create():
    token = test_login()
    response = client.post("/admin/users/create", headers={"Authorization": token}, json={
        "username": "Joef",
        "department": "Testing",
        "role": "basic",
        "password": "smith"
    })
    assert response.status_code == 200
    json = response.json()
    assert json['username'] == "Joef"
    assert json['department'] == "Testing"
    assert json['role'] == "basic"

# Base.metadata.drop_all(bind=engine)
