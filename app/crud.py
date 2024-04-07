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

def get_bookings_on_date(db, d: date):
    return db.query(models.Booking).filter(models.Booking.date == d).all()

def get_todays_booking(db, uid: int):
    return db.query(models.Booking).filter(models.Booking.date == date.today() and models.Booking.owner_id == uid).first()

def get_num_bookings_on_date(db, d: date):
    return len(get_bookings_on_date(db, d))

def create_booking(db: Session, booking: schemas.BookingCreate, uid: int):
    db_booking = models.Booking(**booking.dict(), owner_id=uid)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking
    

def get_seat(db: Session, sid: int):
    return db.query(models.Seat).filter(models.Seat.id == sid).first()

def get_num_seats(db: Session):
    return len(db.query(models.Seat).all())