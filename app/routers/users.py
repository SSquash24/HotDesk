from typing import Annotated

from fastapi import (
    APIRouter, Depends
)

from app import crud, schemas
from app.dependencies import (
    get_current_user, get_db
)


router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/me", response_model=schemas.User)
def read_current_user(user: Annotated[schemas.User, Depends(get_current_user)]):
    return user


@router.post("/password")
async def change_password(
    user: Annotated[schemas.User, Depends(get_current_user)],
    password: str,
    db = Depends(get_db)
):
    return crud.update_password(db, user.id, password)

