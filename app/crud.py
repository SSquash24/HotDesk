# create, read, update, delete methods here
# not sure if we need a separate dummy version for testing

# Code below is for testing purposes, will need to be modified!

from datetime import date

from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, uid: int):
    """
    Retrieves user based on the uid
    """
    return db.query(models.User).filter(models.User.id == uid).first()


def get_user_by_username(db: Session, username: str):
    """
    Retrieves user based on the username
    """
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password + "insert hashing here"
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_booking(db: Session, bid: int): # gets booking by id
    return db.query(models.Booking).filter(models.Booking.id == bid).first()

def get_bookings_by_user(db: Session, uid: int):
    return db.query(models.Booking).filter(models.Booking.owner_id == uid).all()

def get_bookings_on_date(db: Session, d: date):
    return db.query(models.Booking).filter(models.Booking.date == d).all()

def get_bookings_by_user_on_date(db: Session, uid: int, d:date):
    return db.query(models.Booking).filter(models.Booking.owner_id == uid).filter(models.Booking.date == d).first()

def get_todays_booking(db: Session, uid: int):
    return db.query(models.Booking).filter(models.Booking.date == date.today() and models.Booking.owner_id == uid).first()

def get_num_bookings_on_date(db: Session, d: date):
    return len(get_bookings_on_date(db, d))

def create_booking(db: Session, booking: schemas.BookingCreate, uid: int):
    db_booking = models.Booking(**booking.model_dump(), owner_id=uid)
    check = get_bookings_by_user_on_date(db, uid, db_booking.date)
    if check:
        return -1
    if get_num_bookings_on_date(db, db_booking.date) >= get_num_seats(db):
        return -2
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def delete_booking_on_date(db: Session, uid: int, d: date):
    db_booking = get_bookings_by_user_on_date(db, uid, d)
    if not db_booking:
        return -1
    db.delete(db_booking)
    db.commit()
    return 1
    
def assign_seat_to_booking(db: Session, bid: int, sid: int): # assigns the seat with id "sid" to the booking with id "bid" and returns that booking
    booking = get_booking(db, bid)
    if not booking:
        return booking
    booking.seat_id = sid
    db.commit()
    db.refresh(booking)
    return booking

def get_seat(db: Session, sid: int):
    return db.query(models.Seat).filter(models.Seat.id == sid).first()

def get_num_seats(db: Session):
    return len(db.query(models.Seat).all())