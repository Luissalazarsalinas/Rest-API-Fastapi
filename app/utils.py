# Password hashing 
from passlib.context import CryptContext

# Instance 
pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")

# hashing the password
def Hash(password:str):
    return pwd_context.hash(password)

# valid the password credenctial 
def verify(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)
    