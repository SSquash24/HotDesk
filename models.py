# pydantic models here

from datetime import date
from typing import Optional

from pydantic import BaseModel, FutureDate



# base classes: contains common attributes
# create classes: contains attributes input from user for creation of object

class UserBase(BaseModel):
    username: str
    department: str | None

class User(UserBase):
    id: int

class UserCreate(UserBase):
    pass

class BookingBase(BaseModel):
    seat: Optional[str]
    date: date

class Booking(BookingBase):
    id: int
    owner_id: int

class BookingCreate(BookingBase):
    date: FutureDate

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    uid: int | None = None
