from datetime import date
from typing import Annotated


from fastapi import (
    APIRouter, Depends, HTTPException, Path, status
)

from app import crud, schemas

from app.dependencies import (
    get_current_user, verify_token, get_db
)


router = APIRouter(
    prefix="/seats",
    tags=["seats"],
)



@router.get("/me", response_model=schemas.Seat)
def read_current_seat_on_date(
    user: Annotated[schemas.User, Depends(get_current_user)],
    d: date,
    db = Depends(get_db)
):
    booking = crud.get_bookings_by_user_on_date(db, user.id, d)
    if (not booking):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No booking on date")
    if (not booking.seat):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No seat assigned yet")
    return booking.seat

@router.get("/dept", response_model=list[schemas.Seat])
def read_seats_of_colleagues(
    user: Annotated[schemas.User, Depends(get_current_user)],
    d: date,
    db = Depends(get_db)
):
    bookings = crud.get_bookings_by_dept_on_date(db, user.department, d)
    if(not bookings):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="No colleagues booked on date")
    return [b.seat for b in bookings if b.seat]

@router.get("/{seat_id}", 
         response_model=schemas.Seat, 
         dependencies=[Depends(verify_token)])
def read_seat(
    seat_id: Annotated[int, Path(title="ID of seat")], 
    db = Depends(get_db)
):
    return crud.get_seat(db, seat_id)