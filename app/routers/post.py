# Route to create, retrive, update and delete posts
from fastapi import APIRouter, status, Depends, HTTPException, Response
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, oauth2, schemas, utils
from app.database import get_db

# Routers
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# retrive all posts and include parameters
@router.get("/", response_class= List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user),
limit: int = 10, skip: int = 0, search:str = ""): 
    
    #post = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit=limit).offset(skip).all()
    
    # group by query
    result = db.query(
        models.Post,
        func.count(models.Post.id).labes("votes")
    ).join(
        models.Vote, 
        models.Post.id == models.Vote.post_id,
        isouter = True
    ).group_by(models.Post.id).filter(
        models.Post.title.contains(search)
    ).limit(limit=limit).offset(skip).all()

    return result

# Create posts
@router.post("/", status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):

    # create new post
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    # push the new data into the database
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

# Get data per id
@router.get("/{id}", response_model= schemas.PostOut)
def get_post_id(id:int, db: Session = Depends(get_db), currect_user:int = Depends(oauth2.get_current_user)):

    # query 
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(
        models.Post,
        func.count(models.Post.id).labes("votes")
    ).join(
        models.Vote, 
        models.Post.id == models.Vote.post_id,
        isouter = True
    ).group_by(models.Post.id).filter(models.Post.id == id).first()

    # if don't exist the post
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id{id} was not found"
        )
    return post

# Update a posts 
@router.put("/{id}", response_model= schemas.Post)
def update_post(id: int, update_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail= f"post with id: {id} does not exist")
    
    # update only my own posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
        detail = f"Not authorized to perform requested action")

    post_query.update(update_post.dict(), synchronize_session = False)

    # Commint cha nges to the database
    db.commit()

    return post_query.first()

# # Delete a post
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail= f"post with id: {id} does not exist")

    # Delete only my own posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN,
        detail = "Not authorized to perform requested action")
    
    post_query.delete(synchronize_session = False)
    # Commit changes to the database
    db.commit()

    return Response(status_code = status.HTTP_204_NO_CONTENT)


