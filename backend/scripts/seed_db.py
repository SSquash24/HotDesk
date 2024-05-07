import argparse
from datetime import date, timedelta
from pathlib import Path
from random import Random

from faker import Faker

from app import models, config, crud, schemas
from app.dependencies import ContextManager, ADMIN_USER_SCHEMA
from app.schemas import UserCreate
from scripts.init_db import reset_db

DEFAULT_EMPLOYEES = 10
DEFAULT_DEPTS = 3
DEFAULT_BOOKINGS = 6
DEFAULT_DAYS = 5

rand = Random(config.RNG_SEED)
fake = Faker()
Faker.seed(config.RNG_SEED)

def seed_db(
    seats_path: str,
    num_employees: int = DEFAULT_EMPLOYEES, 
    num_depts: int = DEFAULT_DEPTS,
    num_bookings: int = DEFAULT_BOOKINGS,
    num_days: int = DEFAULT_DAYS, 
):
    with open(seats_path, "r") as f:
        name, img_path = f.readline().strip().split(",")
        seat_coords = [[float.fromhex(x) for x in coord.split(',')] 
                       for coord in f.readlines()]
    with ContextManager() as db:
        db_users = []
        for i in range(num_employees):
            user_schema = UserCreate(
                username=fake.name(), 
                department=f"Department {rand.randint(1,num_depts)}",
                role="user",
                password="password"
            )
            db_user = crud.create_user(db, user_schema)
            db_users.append(db_user)

        plan = schemas.PlanCreate(name=name, path=img_path)
        db_plan = crud.create_plan(db, plan)
        for i,(x,y) in enumerate(seat_coords):
            crud.create_seat(db, 
                schemas.SeatCreate(
                    name=str(i), x=x, y=y, plan_id=db_plan.id
                )
            )
        for i in range(num_days):
            day = date.today() + timedelta(i+1)
            for user in rand.sample(db_users, num_bookings):
                crud.create_booking(db, 
                    schemas.BookingCreate(seat_id=None, date=day), 
                    uid=user.id
                )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Seeds the database with fake users, bookings and seats")
    parser.add_argument("seats_path", help="Path to seats",
                        type=Path)
    parser.add_argument("-e","--num_employees", 
                        help="Number of employees to generate",
                        type=int, default=DEFAULT_EMPLOYEES)
    parser.add_argument("-d","--num_depts", help="Number of departments",
                        type=int, default=DEFAULT_DEPTS)
    parser.add_argument("-b","--num_bookings", help="Number of bookings",
                        type=int, default=DEFAULT_BOOKINGS)
    parser.add_argument("-a","--num_days", 
                        help="Number of days to fill bookings for",
                        type=int, default=DEFAULT_DAYS)
    args = parser.parse_args()
    
    if(args.num_bookings > args.num_employees):
        parser.error("Number of bookings must be less than number of employees")

    if(args.num_depts > args.num_employees):
        parser.error("Number of departments must be less than number of employees")

    seed_db(args.seats_path, args.num_employees, args.num_depts, 
            args.num_bookings, args.num_days)
    


