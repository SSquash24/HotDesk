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
    return [b for b in bookings.values() if b.uid == uid]

def get_bookings_on_date(db, d: date):
    bookings = db["bookings"]
    return [b for b in bookings.values() if b.date == d]


def create_booking(db, booking: BookingCreate, uid: int):
    bookings = db["bookings"]
    bid = len(bookings)
    bookings[bid] = Booking(id=bid, owner_id=uid, **booking.model_dump())
    return bookings[bid]
    


# # login_creds: list of [username]
# #   verifies the login detail       s are correct, and return valid users UID
# #   if it is incorrect returns UID -1
# def users_getUID(login_creds):
#     uid = users.get(login_creds[0])
#     if uid == None:
#         return -1
#     return uid

# def users_isValidUID(uid):
#     return uid in users.values()

# def users_getUsername(uid):
#     return uidToUsername[uid]

# def office_getBooking(uid):
#     return bookings_today.get(uid)

# def office_tryBook(uid, Day: date):
#     if Day > date.today():
#         return None
#     return "Cannot book into the past!"