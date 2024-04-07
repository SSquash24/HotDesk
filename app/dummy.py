from datetime import date
from app.models import User, Booking, Seat

dummy_users = {
    0: User(**{
        "id": 0,
        "username": "James",
        "department": "HR",
        "hashed_password": "password"+ "insert hashing here"
    }), 
    1: User(**{
        "id": 1,
        "username": "Jack",
        "department": "Finance",
        "hashed_password": "password"+ "insert hashing here"
    }), 
    2: User(**{
        "id": 2,
        "username": "Sarah",
        "department": "Finance",
        "hashed_password": "password"+ "insert hashing here"
    })
}

dummy_bookings = {
    0: Booking(**{
        "id": 0,
        "seat_id": 0,
        "date": date.today(),
        "owner_id": 0
    }), 
    1: Booking(**{
        "id": 1,
        "seat_id": 1,
        "date": date.today(),
        "owner_id": 2
    })
}

dummy_seats = {
    0: Seat(
        name = "A7",
        x = 0.0,
        y = 1.0,
        id = 0,
    ),
    1: Seat(
        name = "B4",
        x = 1.0,
        y = 0.0,
        id = 1,
    ),
}

dummy_db = {"users": dummy_users, "bookings": dummy_bookings, "seats": dummy_seats}