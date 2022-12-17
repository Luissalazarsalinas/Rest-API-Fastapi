from fastapi import HTTPException, status, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session
from app import models, schemas, utils
from app.database import get_db

# new path former
# add prefixe to resume he route
router = APIRouter(
    prefix = "/users",
    tags= ["Users"]
)

# first query
@router.get("/", response_model= List[schemas.UserOut])
def create_database(db: Session = Depends(get_db)):
    # sql query: SELECT * FROM posts
    user = db.query(models.User).all()

    return user

# # Create a new user
@router.post("/", status_code= status.HTTP_201_CREATED, response_model = schemas.UserOut)
def user_created(user: schemas.Users, db: Session = Depends(get_db)):

    # Hahs the password - User password
    hash_password = utils.Hash(user.password)
    user.password = hash_password 
    # Create user
    new_user = models.User(**user.dict())

    # Commint info to the database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model= schemas.UserOut)
def get_user(id : int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail= f"User with id: {id} does not exist")
    
    return user 