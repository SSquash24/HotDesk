# pydantic models here

from datetime import date
from typing import Annotated, Optional

from numpy import format_float_positional
from pydantic import AfterValidator, BaseModel, Field, FilePath, FutureDate

def check_date_in_future(v: date):
    assert date.today() <= v, "Date should be in the future"
    return v
# database models: 
# base classes: contains common attributes
# create classes: contains attributes input from user for creation of object

class UserBase(BaseModel):
    username: str
    department: str | None
    role: str

class User(UserBase):
    id: int
    hashed_password: str
    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str
    # pass

class BookingBase(BaseModel):
    seat_id: Optional[int] = Field(None, description="Seat ID")
    date: date

class Booking(BookingBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class BookingCreate(BookingBase):
    date: FutureDate

class SeatBase(BaseModel):
    name: str
    x: float
    y: float
    plan_id: int
    
class Seat(SeatBase):
    id: int
    
    class Config:
        from_attributes = True

class SeatCreate(SeatBase):
    pass

class PlanBase(BaseModel):
    name: str
    path: FilePath

class Plan(PlanBase):
    id: int
    class Config:
        from_attributes = True

class PlanCreate(PlanBase):
    pass

# other models:
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    uid: int | None = None
    role: str = ""
