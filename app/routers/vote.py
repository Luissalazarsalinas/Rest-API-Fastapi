from fastapi import Response, HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, oauth2, models

# Creagte the router
router = APIRouter(
    prefix="/votes",
    tags=["VOTES"]
)

# endpoint
@router.post("/", status_code=status.HTTP_201_CREATED)
def votes(vote: schemas.Votes, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # Evalute if the post alredy exist or not
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
        detail=f"Post with id: {vote.post_id} does not exist")

    # Query votes 
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
    models.Vote.user_id == current_user.id)

    found_vote = vote_query.first()

    # Evalute dir for add or delete a vote
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException( status_code= status.HTTP_409_CONFLICT,
            detail= f"user {current_user.id} has already voted on post{vote.post_id}")
        
        new_vote = models.Vote(vote.post_id, current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
            detail="The vote does not exist")
        
        vote_query.delete(synchronize_session= False)
        db.commit()

        return {"message": "successfully deleted vote"}
