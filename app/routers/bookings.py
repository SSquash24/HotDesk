from typing import Annotated
from datetime import date

from fastapi import (
    APIRouter, Depends, HTTPException, status
)

from app import crud, schemas, config
from app.dependencies import (
    get_current_user, verify_token, get_db
)


router = APIRouter(
    prefix="/bookings",
    tags=["bookings"],
)


@router.get("/me", response_model=list[schemas.Booking])
def read_current_bookings(
    user: Annotated[schemas.User, Depends(get_current_user)], 
    db = Depends(get_db)
):
    return crud.get_bookings_by_user(db, user.id)

@router.get("/date", 
         response_model=list[schemas.Booking], 
         dependencies=[Depends(verify_token)])
def read_bookings_on_date(date: date, db = Depends(get_db)):
    return crud.get_bookings_on_date(db, date)

@router.get("/count", 
         response_model=int, 
         dependencies=[Depends(verify_token)])
def read_num_bookings_on_date(date: date, db = Depends(get_db)):
    return crud.get_num_bookings_on_date(db, date)

@router.get("/today", response_model=schemas.Booking)
def read_todays_booking(
    user: Annotated[schemas.User, Depends(get_current_user)], 
    db = Depends(get_db)
):
    booking = crud.get_todays_booking(db, user.id)
    if (not booking):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No booking today")
    return booking

@router.get("/vacancies", 
         response_model=int, 
         dependencies=[Depends(verify_token)])
def read_num_vacancies_on_date(date: date, db = Depends(get_db)):
    return (crud.get_num_seats_in_plan(db, config.CURR_PLAN) 
            - crud.get_num_bookings_on_date(db, date))

@router.post("/book", response_model=schemas.Booking)
async def book(
    booking: schemas.BookingCreate, 
    user: Annotated[schemas.User, Depends(get_current_user)], 
    db = Depends(get_db)
):
    """ will not book the same person twice on the same day, nor overbook """
    curr_booking = crud.get_bookings_by_user_on_date(db, user.id, booking.date)
    if (curr_booking):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking already exists"
        )
    if (crud.get_num_seats_in_plan(db, config.CURR_PLAN) - 
        crud.get_num_bookings_on_date(db, booking.date) <= 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking full"
        )
    return crud.create_booking(db, booking, user.id)

@router.delete("/me/delete")
async def delete_booking(
    d: date, 
    user: Annotated[schemas.User, Depends(get_current_user)], 
    db = Depends(get_db)
):
    db_booking = crud.get_bookings_by_user_on_date(db, user.id, d)
    if (not db_booking):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No booking to delete"
        )
    crud.delete_booking_on_date(db, user.id, d)
    return "Successfully deleted booking"