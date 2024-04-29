from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Float, null
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
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=True)
    date = Column(Date)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship(
        "User", back_populates="bookings", foreign_keys=[owner_id]
    )

    seat = relationship(
        "Seat", back_populates="bookings", foreign_keys=[seat_id]
    )

class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True)
    plan_id = Column(Integer, ForeignKey("plans.id"))
    name = Column(String)
    x = Column(Float)
    y = Column(Float)

    bookings = relationship("Booking", back_populates="seat")
    plan = relationship("Plan", back_populates="seats", foreign_keys=[plan_id])

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True)
    path = Column(String)
    name = Column(String)

    seats = relationship("Seat", back_populates="plan")
