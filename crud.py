# create, read, update, delete methods here
# not sure if we need a separate dummy version for testing

# Code below is for testing purposes, will need to be modified!

from datetime import date


from models import Booking, BookingCreate, UserCreate, User


def get_user(db, uid: int):
    """
    Retrieves user based on the uid
    """
    users = db["users"]
    return users.get(uid)

def get_user_by_username(db, username: str):
    """
    Retrieves user based on the username
    """
    users = db["users"]
    for user in users.values():
        if(user.username == username):
            return user
    return None

def get_booking(db, bid: int):
    bookings = db["bookings"]
    return bookings.get(bid)

def get_bookings_by_user(db, uid: int):
    bookings = db["bookings"]
    return [b for b in bookings.values() if b.owner_id == uid]

def get_bookings_on_date(db, d: date):
    bookings = db["bookings"]
    return [b for b in bookings.values() if b.date == d]

def get_todays_booking(db, uid: int):
    bookings = db["bookings"]
    today = [b for b in bookings.values() if b.date == date.today() and b.owner_id == uid]
    if (today):
        return today[0]
    return None

def get_num_bookings_on_date(db, d: date):
    return len(get_bookings_on_date(db, d))

def create_booking(db, booking: BookingCreate, uid: int):
    bookings = db["bookings"]
    bid = len(bookings)
    bookings[bid] = Booking(id=bid, owner_id=uid, **booking.model_dump())
    return bookings[bid]
    
