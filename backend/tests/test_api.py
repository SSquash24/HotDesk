
from datetime import date, timedelta

from app.dependencies import ADMIN_USER_SCHEMA, DUMMY_USER_SCHEMA






# Login -------------------------------------------------------------

def test_admin_login(admin_login):
    assert admin_login.status_code == 200


def test_login_bad_user(client):
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

def test_user_me_bad_token(client):
    response = client.get("/users/me", headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_user_me_(client, admin_token):
    response = client.get("/users/me", 
                          headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200

    json = response.json()
    assert json['username'] == ADMIN_USER_SCHEMA.username
    assert json['department'] == ADMIN_USER_SCHEMA.department
    assert json['role'] == ADMIN_USER_SCHEMA.role


def test_user_password_bad_token(client):
    response = client.get(
        f"/users/password?password={ADMIN_USER_SCHEMA.password}", 
        headers={"Authorization": "a bad one!"}
    )
    assert response.status_code == 405
    assert response.json() == {
        "detail": "Method Not Allowed"
    }

def test_user_password(client, user_token):
    dummy_pass = "dummypw"
    response = client.post(
        f"/users/password?password={dummy_pass}", 
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200
    response = client.post(
        f"/users/password?password={DUMMY_USER_SCHEMA.password}", 
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 200


# ADMIN CALLS -----------------------------------------------------------

def test_admin_user_create(client, admin_token):
    response = client.post("/admin/users/create", 
                           headers={"Authorization": f"Bearer {admin_token}"}, 
                           json={
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


def test_login_basic(user_login):
    assert user_login.status_code == 200


def test_basic_user_create_fail(client, user_token):
    response = client.post("/admin/users/create", 
                           headers={"Authorization": f"Bearer {user_token}"}, 
                           json={
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

future_day = str(date.today()+timedelta(days=10))
tomorrow = str(date.today() + timedelta(days=1))
today = str(date.today())


def test_bookings_book_bad_token(client):
    response = client.post("/bookings/book/", headers={"Authorization": "a bad one!"}, json={
        "date": tomorrow
    })
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_book(single_booking):
    assert single_booking.status_code == 200
    assert single_booking.json()['date'] == future_day

def test_bookings_book_repeat(client, user_token):
    response = client.post(
        "/bookings/book/", 
        headers={"Authorization": f"Bearer {user_token}"}, 
        json={"date": tomorrow}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Booking already exists"
    }

def test_bookings_book_filled(client, admin_token):
    response = client.post(
        "/bookings/book/", 
        headers={"Authorization": f"Bearer {admin_token}"}, 
        json={"date": tomorrow}
    )
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Booking full"
    }



def test_bookings_count_bad_token(client):
    response = client.get(f"/bookings/count?date={tomorrow}", 
                          headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_count_0(client, user_token):
    response = client.get(f"/bookings/count?date={today}", 
                          headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json() == 0

def test_bookings_count_1(client, user_token):
    response = client.get(f"/bookings/count?date={tomorrow}", 
                          headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json() == 1



def test_bookings_vacancies_bad_token(client):
    response = client.get(f"/bookings/vacancies?date={tomorrow}", 
                          headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_vacancies_0(client, user_token):
    response = client.get(f"/bookings/vacancies?date={tomorrow}", 
                          headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json() == 0

def test_bookings_vacancies_1(client, user_token):
    response = client.get(f"/bookings/vacancies?date={today}", 
                          headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json() == 1



def test_bookings_me_bad_token(client):
    response = client.get("/bookings/me", headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_me_booked(client, user_token, single_booking):
    response = client.get("/bookings/me", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 2
    assert json[0]['date'] == tomorrow
    assert json[1]['date'] == future_day

def test_bookings_me_empty(client, admin_token):
    response = client.get("/bookings/me", 
                          headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == 200
    assert response.json() == []



def test_bookings_date_bad_token(client):
    response = client.get(f"/bookings/date?date={tomorrow}", 
                          headers={"Authorization": "a bad one!"})
    assert response.status_code == 401
    assert response.json() == {
        "detail": "Not authenticated"
    }

def test_bookings_date_empty(client, user_token):
    response = client.get(f"/bookings/date?date={today}", 
                          headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    assert response.json() == []

def test_bookings_date_full(client, user_token):
    response = client.get(f"/bookings/date?date={tomorrow}", 
                          headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == 200
    json = response.json()
    assert len(json) == 1
    assert json[0]['date'] == tomorrow



