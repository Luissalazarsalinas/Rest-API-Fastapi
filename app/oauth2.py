from jose import JWSError, jwt
from datetime import datetime, timedelta
from app import models, schemas
from app.database import get_db
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.config import settings

# soterd token generated
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# main variables to create a jwt
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

# create a json web token 
def create_access_token(data:dict):

    # copy from data
    to_encode = data.copy()

    #time of expire
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)

    # update date
    to_encode.update({"expire": expire})

    # jwt
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encode_jwt

# valid the token created
# helper funtions
def verify_access_token(token:str, credentials_exception):

    try:

        # decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])

        # Verify by user id
        id = payload.get("user_id")

        # if don't exist the user
        if id is None:
            raise credentials_exception
        # verofy token 
        token_data = schemas.TokenData(id=id)
    except JWSError:
        raise credentials_exception
    
    return token_data

# get currenct user for get a resource after valid the token
def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    # Handled credential exception
    credentials_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= f"Could not validated credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    # verify the token
    token_var = verify_access_token(token, credentials_exception)

    # query for return the user recurse
    user = db.query(models.User).filter(models.User.id == token).first()

    return user