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
    seat: Optional[str] = Field("", description="Seat name")
    date: date

class Booking(BookingBase):
    id: int
    owner_id: int

class BookingCreate(BookingBase):
    date: FutureDate

# other models:
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    uid: int | None = None
