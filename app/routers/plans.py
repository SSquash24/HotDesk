from typing import Annotated

from fastapi import (
    APIRouter, Depends, HTTPException, Path, status
)
from fastapi.responses import FileResponse

from app import crud, schemas
from app.dependencies import (
    verify_token, get_db
)

router = APIRouter(
    prefix="/plans",
    tags=["plans"],
)


@router.get("/{plan_id}", 
            response_model=schemas.Plan, 
            dependencies=[Depends(verify_token)])
def read_plan(
    plan_id: Annotated[int, Path(title="ID of plan")], 
    db = Depends(get_db)
):
    plan = crud.get_plan(db, plan_id)
    if (not plan):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="No plan with given id"
        )
    return plan

@router.get("/{plan_id}/seats",
            response_model=list[schemas.Seat], 
            dependencies=[Depends(verify_token)],
            tags=["seats"])
def read_seats_in_plan(
    plan_id: Annotated[int, Path(title="ID of plan")], 
    db = Depends(get_db)
):
    return crud.get_seats_in_plan(db, plan_id)

@router.get("/{plan_id}/image", 
            response_model=schemas.Plan, 
            dependencies=[Depends(verify_token)])
def read_plan_img(
    plan_id: Annotated[int, Path(title="ID of plan")], 
    db = Depends(get_db)
):
    path = crud.get_plan_path(db, plan_id)
    return FileResponse(path)