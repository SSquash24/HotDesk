
from datetime import date
from typing import Annotated

from fastapi import (
    APIRouter, Depends, Path, HTTPException, status
)
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.algo.util import evaluate_assignment, metrics
from app.config import ALGO_METRIC
from app.dummy import dummy_db
from app.dependencies import (
   ADMIN_USER_SCHEMA, verify_admin,  get_db
)

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(verify_admin)]
)



# testing purposes --- initializes some users into the database if it is empty
def create_dummy(db):
    for user in dummy_db["users"].values():
        db.add(user)
    for booking in dummy_db["bookings"].values():
        db.add(booking)
    for seat in dummy_db["seats"].values():
        db.add(seat)
    db.commit()
        
    
# testing purposes --- clears database
def reset_db(db):
    db.query(models.User).delete()
    db.query(models.Booking).delete()
    db.query(models.Seat).delete()
    db.commit()


# testing purposes --- clears and initializes database with the dummy database

@router.post("/reset/init")
async def initialise_dummy(db = Depends(get_db)):
    reset_db(db)
    create_dummy(db)
    return "Database initialised with dummy values"

@router.post("/reset/all")
async def reset(db = Depends(get_db)):
    reset_db(db)
    crud.create_user(db, ADMIN_USER_SCHEMA)
    return "Database reset to empty state"


@router.get(
    "/users/{user_id}", 
    response_model=schemas.User, 
    tags=["users"]
)
def read_user(
    user_id: Annotated[int, Path(title="ID of user")], 
    db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if (not db_user):
        raise HTTPException(status_code=400, 
                            detail="User with ID does not exist")
    return db_user

@router.post(
    "/users/create", 
    response_model=schemas.User, 
    tags=["users"]
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db=db, user=user)


# unsure if this is needed here specifically but being able to assign a booking to a specific seat is needed as initially
# bookings will come with no seat (default value -1) before the algorithm assigns them to everyone
@router.put(
    "/bookings/assign/{booking_id}", 
    tags=["bookings"]
)
async def assign_single(
    booking_id: Annotated[int, Path(title="ID of booking")], 
    seat_id: int, 
    db = Depends(get_db)
):
    try:
        db_booking = crud.update_booking_with_seat(db, booking_id, seat_id)
        return db_booking
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )

@router.post(
    "/bookings/assign", 
    tags=["bookings"]
)
async def assign_seats_on_date(
    d: date,
    db = Depends(get_db)
):
    crud.update_bookings_on_date(db, d)
    return 

@router.get(
    "/bookings/score", 
    tags=["bookings"]
)
async def calculate_score_for_date(
    d: date, 
    db = Depends(get_db)
):
    return crud.get_booking_score(db, d)