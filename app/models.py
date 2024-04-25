from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float
from sqlalchemy.orm import relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    department = Column(String, nullable=True)
    role = Column(String, nullable=False)
    hashed_password = Column(String)

    bookings = relationship("Booking", back_populates="owner")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)
    seat_id = Column(Integer, index=True, default=-1)
    date = Column(Date)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="bookings", foreign_keys=[owner_id])

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    x = Column(Float)
    y = Column(Float)
