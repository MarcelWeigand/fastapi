from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
#from .config import settings 

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

#video bei 7:09:22
#SECRTET_KEy that resides on our server
#Algorithm
#experation time

# SECRET_KEY = settings.secret_key
# ALGORITHM = settings.algorithm
# ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

SECRET_KEY = "5bb7f2f5b51015238386d0894bcc60acde6fd482922f878b6c0a774e0537a373"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: int = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

    except JWTError:
        raise credentials_exception
    
    # returning the id
    return token_data
    

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"could not valid credentilas", headers={"WWW-Authenticate:" "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

#     try:
#         token_data = oauth2.verify_access_token(token, credentials_exception)
#         user = db.query(models.User).get(token_data.id)
#         if not user:
#             raise credentials_exception
#         return user
#     except JWTError:
#         raise credentials_exception