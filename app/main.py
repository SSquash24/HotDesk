# Backend API with FastAPI 

# standard library imports
from typing import Annotated
from datetime import date, datetime, timedelta, timezone

# 3rd party imports
from fastapi import Depends, FastAPI, Path, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
# sqlAlchemy
from sqlalchemy.orm import Session

# local imports
from app import crud, models, schemas
from app.database import SessionLocal, engine
# from app import crud_dummy as crud
from app.dummy import dummy_db


models.Base.metadata.create_all(bind=engine)

# secret key used for encoding session data
# should be in some .env file in production, not committed
# but this works for now
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "6d7b5968fccbc2b4d484280030d9424536091a64a9bd7c167e91ea18aaa98312"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

app = FastAPI()


origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_db():
    # return dummy_db
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# testing purposes --- initializes some users into the database if it is empty
def create_dummy(db):
    for user in dummy_db["users"].values():
        db.add(user)
    for booking in dummy_db["bookings"].values():
        db.add(booking)
    for seat in dummy_db["seats"].values():
        db.add(seat)
    db.commit()
        
    
# testing purposes --- clears database
def clear_db(db):
    db.query(models.User).delete()
    db.query(models.Booking).delete()
    db.query(models.Seat).delete()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(db, username: str, password: str):
    user = crud.get_user_by_username(db, username)
    if not user:
        return False
    # fix hashing at some point
    # if not (password + "insert hashing here" == user.hashed_password):
    #     return False
    return user

async def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("sub")
        role: str = payload.get("role")
        if uid is None or role is None:
            raise CREDENTIALS_EXCEPTION
        token_data = schemas.TokenData(uid=int(uid), role=role)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    return token_data

async def get_current_user(token_data: Annotated[str, Depends(verify_token)], db = Depends(get_db)):
    user = crud.get_user(db, token_data.uid)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user

async def verify_admin(token_data: Annotated[str, Depends(verify_token)]):
    if(token_data.role != "admin"):
        raise CREDENTIALS_EXCEPTION

# GET REQUESTS  -----------------------------------------------------------

@app.get("/users/me", response_model=schemas.User)
def read_current_user(user: Annotated[schemas.User, Depends(get_current_user)]):
    return user

@app.get("/bookings/me", response_model=list[schemas.Booking])
def read_current_bookings(
    user: Annotated[schemas.User, Depends(get_current_user)], 
    db = Depends(get_db)
):
    return crud.get_bookings_by_user(db, user.id)

@app.get("/bookings/date", 
         response_model=list[schemas.Booking], 
         dependencies=[Depends(verify_token)])
def read_bookings_on_date(date: date, db = Depends(get_db)):
    return crud.get_bookings_on_date(db, date)

@app.get("/bookings/count", 
         response_model=int, 
         dependencies=[Depends(verify_token)])
def read_num_bookings_on_date(date: date, db = Depends(get_db)):
    return crud.get_num_bookings_on_date(db, date)

@app.get("/bookings/today", response_model=schemas.Booking)
def read_todays_booking(
    user: Annotated[schemas.User, Depends(get_current_user)], 
    db = Depends(get_db)
):
    booking = crud.get_todays_booking(db, user.id)
    if (not booking):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No booking today")
    return booking

@app.get("/bookings/vacancies", 
         response_model=int, 
         dependencies=[Depends(verify_token)])
def read_num_vacancies_on_date(date: date, db = Depends(get_db)):
    return crud.get_num_seats(db) - crud.get_num_bookings_on_date(db, date)

@app.get("/seats/{seat_id}", 
         response_model=schemas.Seat, 
         dependencies=[Depends(verify_token)])
def read_seat(
    seat_id: Annotated[int, Path(title="ID of seat")], 
    db = Depends(get_db)
):
    return crud.get_seat(db, seat_id)


# POST REQUESTS -----------------------------------------------------------


@app.post("/users/", 
          response_model=schemas.User, 
          dependencies=[Depends(verify_admin)])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already exists")
    return crud.create_user(db=db, user=user)

@app.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db = Depends(get_db)
) -> schemas.Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role}, 
        expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")

# testing purposes --- clears and initializes database with the dummy database
@app.post("/setup")
async def init(db = Depends(get_db)):
    clear_db(db)
    create_dummy(db)
    return "cleared and initialized database"

@app.post("/bookings/book", response_model=schemas.Booking)
async def book(
    booking: schemas.BookingCreate, 
    user: Annotated[schemas.User, Depends(get_current_user)], 
    db = Depends(get_db)
):
    """ will not book the same person twice on the same day, nor overbook """
    curr_booking = crud.get_bookings_by_user_on_date(db, user.id, booking.date)
    if (curr_booking):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking already exists"
        )
    if (crud.get_num_seats(db) - 
        crud.get_num_bookings_on_date(db, booking.date) <= 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Booking full"
        )
    return crud.create_booking(db, booking, user.id)


# PUT REQUESTS -----------------------------------------------------------


# unsure if this is needed here specifically but being able to assign a booking to a specific seat is needed as initially
# bookings will come with no seat (default value -1) before the algorithm assigns them to everyone
@app.put("/bookings/assign/{booking_id}", dependencies=[Depends(verify_admin)])
async def assign(
    booking_id: Annotated[int, Path(title="ID of booking")], 
    seat_id: int, 
    db = Depends(get_db)
):
    try:
        db_booking = crud.update_booking_with_seat(db, booking_id, seat_id)
        return db_booking
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )


# DELETE REQUESTS -----------------------------------------------------------

@app.delete("/bookings/delete")
async def delete(
    d: date, 
    user: Annotated[schemas.User, Depends(get_current_user)], 
    db = Depends(get_db)
):
    db_booking = crud.get_bookings_by_user_on_date(db, user.id, d)
    if (not db_booking):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No booking to delete"
        )
    crud.delete_booking_on_date(db, user.id, d)
    return "Successfully deleted booking"