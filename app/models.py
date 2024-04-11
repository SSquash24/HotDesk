from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    department = Column(String, index=True)   
    hashed_password = Column(String)

    bookings = relationship("Booking", back_populates="owner")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    seat_id = Column(Integer, index=True, default=-1)
    date = Column(Date, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="bookings", foreign_keys=[owner_id])

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    x = Column(Float, index=True)
    y = Column(Float, index=True)

class Token(Base):
    __tablename__ = "tokens"

    access_token = Column(String, primary_key=True)
    token_type = Column(String, index=True)

class TokenData(Base):
    __tablename__ = "tokendata"

    uid = Column(Integer, primary_key=True)