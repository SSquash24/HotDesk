# Backend API with FastAPI 
# (I removed all the frontend endpoints with API "equivalents" for demonstration)

# standard library imports
from typing import Annotated
from datetime import date, datetime, timedelta, timezone

# 3rd party imports
from fastapi import Depends, FastAPI, Path, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

# local imports
import crud
from models import Booking, BookingCreate, Seat, User, Token, TokenData
from dummy import dummy_db


# secret key used for encoding session data
# should be in some .env file in production, not committed
# but this works for now
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "6d7b5968fccbc2b4d484280030d9424536091a64a9bd7c167e91ea18aaa98312"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



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
    return dummy_db

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
    # no passwords for now
    # if not verify_password(password, user.hashed_password):
    #     return False
    return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: str = payload.get("sub")
        if uid is None:
            raise credentials_exception
        token_data = TokenData(uid=int(uid))
    except JWTError:
        raise credentials_exception
    user = crud.get_user(db, token_data.uid)
    if user is None:
        raise credentials_exception
    return user


# GET REQUESTS  -----------------------------------------------------------


@app.get("/users/me", response_model=User)
async def read_current_user(user: Annotated[User, Depends(get_current_user)]):
    return user

@app.get("/bookings/me", response_model=list[Booking])
async def read_current_bookings(user: Annotated[User, Depends(get_current_user)], db = Depends(get_db)):
    return crud.get_bookings_by_user(db, user.id)

@app.get("/bookings/date", response_model=list[Booking], dependencies=[Depends(oauth2_scheme)])
async def read_bookings_on_date(date: date, db = Depends(get_db)):
    return crud.get_bookings_on_date(db, date)

@app.get("/bookings/count", response_model=int, dependencies=[Depends(oauth2_scheme)])
async def read_num_bookings_on_date(date: date, db = Depends(get_db)):
    return crud.get_num_bookings_on_date(db, date)

@app.get("/bookings/today", response_model=Booking)
async def read_todays_booking(user: Annotated[User, Depends(get_current_user)], db = Depends(get_db)):
    booking = crud.get_todays_booking(db, user.id)
    if (not booking):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No booking today")
    return booking

@app.get("/bookings/vacancies", response_model=int, dependencies=[Depends(oauth2_scheme)])
async def read_num_vacancies_on_date(date: date, db = Depends(get_db)):
    return crud.get_num_seats(db) - crud.get_num_bookings_on_date(db, date)

@app.get("/seats/{seat_id}", response_model=Seat, dependencies=[Depends(oauth2_scheme)])
async def read_seat(seat_id: Annotated[int, Path(title="ID of seat")], db = Depends(get_db)):
    return crud.get_seat(db, seat_id)


# POST REQUESTS -----------------------------------------------------------



@app.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db = Depends(get_db)
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")




@app.post("/bookings/book", response_model=Booking)
async def book(booking: BookingCreate, user: Annotated[User, Depends(get_current_user)], db = Depends(get_db)):
    booking = crud.create_booking(db, booking, user.id)
    return booking
