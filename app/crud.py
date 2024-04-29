# create, read, update, delete methods here
# not sure if we need a separate dummy version for testing


from datetime import date

from sqlalchemy import delete, select, func
from sqlalchemy.orm import Session

from app import models, schemas


def get_user(db: Session, uid: int):
    """
    Retrieves user based on the uid
    """
    return db.scalars(
        select(models.User).where(models.User.id == uid)
    ).first()


def get_user_by_username(db: Session, username: str):
    """
    Retrieves user based on the username
    """
    return db.scalars(
        select(models.User).where(models.User.username == username)
    ).first()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password + "insert hashing here"
    db_user = models.User(
        **user.model_dump(exclude={'password'}),
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_password(db: Session, uid: int, password: str):
    hashed_password = password + "insert hashing here"
    user = get_user(db, uid)
    user.hashed_password = hashed_password
    db.commit()
    db.refresh(user)
    return user

def get_booking(db: Session, bid: int): 
    """ gets booking by id or throws NoResultFound exception if none match
    """
    return db.scalars(
        select(models.Booking).where(models.Booking.id == bid)
    ).one()

def get_bookings_by_user(db: Session, uid: int):
    return db.scalars(
        select(models.Booking).where(models.Booking.owner_id == uid)
    ).all()

def get_bookings_on_date(db: Session, d: date):
    return db.scalars(
        select(models.Booking).where(models.Booking.date == d)
    ).all()

def get_bookings_by_user_on_date(db: Session, uid: int, d: date):
    return db.scalars(
        select(models.Booking)
        .where(models.Booking.owner_id == uid)
        .where(models.Booking.date == d)
    ).first()

def get_todays_booking(db: Session, uid: int):
    return db.scalars(
        select(models.Booking)
        .where(models.Booking.date == date.today())
        .where(models.Booking.owner_id == uid)
    ).first()

def get_num_bookings_on_date(db: Session, d: date):
    return db.scalar(
        select(func.count())
        .select_from(models.Booking)
        .where(models.Booking.date == d)
    )

def create_booking(db: Session, booking: schemas.BookingCreate, uid: int):
    db_booking = models.Booking(**booking.model_dump(), owner_id=uid)
    
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

def delete_booking_on_date(db: Session, uid: int, d: date):
    db.execute(
        delete(models.Booking)
        .where(models.Booking.date == d)
        .where(models.Booking.owner_id == uid)
    )
    db.commit()
    
def update_booking_with_seat(db: Session, bid: int, sid: int): 
    """ 
    Assigns the seat with id "sid" to the booking with id "bid" 
    and returns that booking
    """
    booking = get_booking(db, bid)
    booking.seat_id = sid
    db.commit()
    db.refresh(booking)
    return booking

def create_seat(db: Session, seat: schemas.SeatCreate):
    db_seat = models.Seat(**seat.model_dump())

    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat

def get_seat(db: Session, sid: int):
    return db.scalars(
        select(models.Seat).where(models.Seat.id == sid)
    ).first()

def get_num_seats(db: Session):
    return db.scalar(
        select(func.count())
        .select_from(models.Seat)
    )

def get_seats_in_plan(db: Session, pid: int):
    return db.scalars(
        select(models.Seat).where(models.Seat.plan_id == pid)
    ).all()

def create_plan(db: Session, plan: schemas.PlanCreate):
    db_plan = models.Plan(
        **plan.model_dump(exclude=["path"]), path=str(plan.path)
    )

    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_plan(db: Session, pid: int):
    return db.scalars(
        select(models.Plan).where(models.Plan.id == pid)
    ).first()

def get_plan_path(db: Session, pid: int):
    return db.scalar(
        select(models.Plan.path).where(models.Plan.id == pid)
    )