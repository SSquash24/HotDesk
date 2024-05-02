from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import models, crud
from app.main import app, get_db
from app.routers.admin import ADMIN_USER_SCHEMA
from app.schemas import SeatCreate, PlanCreate

from pydantic import FilePath

from datetime import date, timedelta

# create testing db and client ---------------------------

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

db_plan = crud.create_plan(db, PlanCreate(name="testplan", path=FilePath("tests/testlayout.csv")))
crud.create_seat(db, SeatCreate(
    name= "seat 0",
    x=0.0,
    y=0.0,
    plan_id=db_plan.id
))
db.close()

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()



app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)



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


# ADMIN CALLS -----------------------------------------------------------

def test_admin_user_create():
    token = test_login()
    response = client.post("/admin/users/create", headers={"Authorization": token}, json={
        "username": "Joe",
        "department": "Testing",
        "role": "basic",
        "password": "smith"
    })
    assert response.status_code == 200
    json = response.json()
    assert json['username'] == "Joe"
    assert json['department'] == "Testing"
    assert json['role'] == "basic"


def test_login_basic():
    form_data = {
        "username": "Joe",
        "password": "smith"
    }

    response = client.post("/login", data=form_data, headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    })
    assert response.status_code == 200
    return "bearer " + response.json()['access_token']


def test_basic_user_create_fail():
    token = test_login_basic()
    response = client.post("/admin/users/create", headers={"Authorization": token}, json={
        "username": "Don't",
        "department": "Accept",
        "role": "basic",
        "password": "This"
    })
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Could not validate credentials"
    }


# BOOKINGS CALLS ------------------------------------------------------------

tomorrow = str(date.today() + timedelta(1))
today = str(date.today())


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
    response = client.post("/bookings/book/", headers={"Authorization": token}, json={
        "date": tomorrow
    })
    assert response.status_code == 200
    assert response.json()['date'] == tomorrow

def test_bookings_book_repeat():
    token = test_login()
    response = client.post("/bookings/book/", headers={"Authorization": token}, json={
        "date": tomorrow
    })
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Booking already exists"
    }

def test_bookings_book_filled():
    token = test_login_basic()
    response = client.post("/bookings/book/", headers={"Authorization": token}, json={
        "date": tomorrow
    })
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Booking full"
    }



def test_bookings_count_bad_token():
    response = client.get(f"/bookings/count?date={tomorrow}", headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_count_0():
    token = test_login()
    response = client.get(f"/bookings/count?date={today}", headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json() == 0

def test_bookings_count_1():
    token = test_login()
    response = client.get(f"/bookings/count?date={tomorrow}", headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json() == 1



def test_bookings_vacancies_bad_token():
    response = client.get(f"/bookings/vacancies?date={tomorrow}", headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_vacancies_0():
    token = test_login()
    response = client.get(f"/bookings/vacancies?date={tomorrow}", headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json() == 0

def test_bookings_vacancies_1():
    token = test_login()
    response = client.get(f"/bookings/vacancies?date={today}", headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json() == 1



def test_bookings_me_bad_token():
    response = client.get("/bookings/me", headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_me_booked():
    token = test_login()
    response = client.get("/bookings/me", headers={"Authorization": token})
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1
    assert json[0]['date'] == tomorrow

def test_bookings_me_empty():
    token = test_login_basic()
    response = client.get("/bookings/me", headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json() == []



def test_bookings_date_bad_token():
    response = client.get(f"/bookings/date?date={tomorrow}", headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_date_empty():
    token = test_login()
    response = client.get(f"/bookings/date?date={today}", headers={"Authorization": token})
    assert response.status_code == 200
    assert response.json() == []

def test_bookings_date_full():
    token = test_login()
    response = client.get(f"/bookings/date?date={tomorrow}", headers={"Authorization": token})
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1
    assert json[0]['date'] == tomorrow



