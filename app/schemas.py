## Data validations
from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional

# SCHEMAS
class BasePost(BaseModel):
    title: str
    content: str
    published: bool = True

# Brach  new class for the response
class CreatePost(BasePost):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

# To handled the responde from the api
class Post(BaseModel):
    id: str
    created_at:datetime
    owner_id:int
    owner: UserOut          # To get the user information 

    class Config:
        orm_mode = True

# Postout that include vote info
class PostOut(BaseModel):
    post: Post
    votes: int

    class Config:
        orm_mode = True

# User info
class Users(BaseModel):
    email: EmailStr
    password: str

# USER LOGGING
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Token 
class Token(BaseModel):
    access_token: str
    token_type: str

# token data
class TokenData(BaseModel):
    id: Optional[str] = None

# Votes
class Votes(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)