from typing import Annotated


from fastapi import (
    APIRouter, Depends, Path,
)

from app import crud, schemas

from app.dependencies import (
    verify_token, get_db
)


router = APIRouter(
    prefix="/seats",
    tags=["seats"],
)


@router.get("/{seat_id}", 
         response_model=schemas.Seat, 
         dependencies=[Depends(verify_token)])
def read_seat(
    seat_id: Annotated[int, Path(title="ID of seat")], 
    db = Depends(get_db)
):
    return crud.get_seat(db, seat_id)