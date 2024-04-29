from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app import crud, schemas, config
from app.database import SessionLocal
from jose import JWTError, jwt




oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")



CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

class ContextManager:
    def __init__(self):
        self.db = SessionLocal()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

async def get_db():
    with ContextManager() as db:
        yield db

def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(
            token, config.SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        uid: str = payload.get("sub")
        role: str = payload.get("role")
        if uid is None or role is None:
            raise CREDENTIALS_EXCEPTION
        token_data = schemas.TokenData(uid=int(uid), role=role)
    except JWTError:
        raise CREDENTIALS_EXCEPTION
    return token_data

def get_current_user(
    token_data: Annotated[str, Depends(verify_token)], db = Depends(get_db)
):
    user = crud.get_user(db, token_data.uid)
    if user is None:
        raise CREDENTIALS_EXCEPTION
    return user

def verify_admin(token_data: Annotated[str, Depends(verify_token)]):
    if(token_data.role != "admin"):
        raise CREDENTIALS_EXCEPTION