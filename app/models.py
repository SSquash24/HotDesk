# pydantic models here

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, FutureDate



# database models: 
# base classes: contains common attributes
# create classes: contains attributes input from user for creation of object

class UserBase(BaseModel):
    username: str
    department: str | None

class User(UserBase):
    id: int
    # hashed_password: str

class UserCreate(UserBase):
    # password: str
    pass

class BookingBase(BaseModel):
    seat_id: Optional[int] = Field(None, description="Seat ID")
    date: date

class Booking(BookingBase):
    id: int
    owner_id: int

class BookingCreate(BookingBase):
    date: FutureDate

class SeatBase(BaseModel):
    name: str
    x: float
    y: float

class Seat(SeatBase):
    id: int

class SeatCreate(SeatBase):
    pass

# other models:
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    uid: int | None = None
