from datetime import date
from models import User, Booking

dummy_users = {
    0: User(**{
        "id": 0,
        "username": "James",
        "department": "HR",
    }), 
    1: User(**{
        "id": 1,
        "username": "Jack",
        "department": "Finance",
    }), 
    2: User(**{
        "id": 2,
        "username": "Sarah",
        "department": "Finance",
    })
}

dummy_bookings = {
    0: Booking(**{
        "id": 0,
        "seat":"A7",
        "date": date.today(),
        "owner_id": 0
    }), 
    1: Booking(**{
        "id": 1,
        "seat":"B4",
        "date": date.today(),
        "owner_id": 2
    })
}

dummy_db = {"users": dummy_users, "bookings": dummy_bookings}