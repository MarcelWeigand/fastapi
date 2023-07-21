from .. import models,schemas, utils, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
#from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from ..database import get_db
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)



#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
#@router.get("/", response_model=List[schemas.PostOUT])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str]=""):
    print(limit)
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    # only return the posts from the current user
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), current_user: schemas.TokenData = Depends(oauth2.get_current_user)): #post is stored in the Post object
    # new_post = models.Post(**post.dict())  # put all columns in a dict and unpack it so that you dont have to code every column
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, title=post.title,
        content=post.content,
        published=post.published,)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schemas.PostOut) #id is a path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with ih: {id} was not found"}

    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform this action")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id: {id} does not exist")
    
    # nur der die posts des eingeloggten users können gelöscht werden
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform this action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id: {id} does not exist")
    # post_query.update({'title': 'my updated title', 'content': 'my updated content'}, synchronize_session=False)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to perform this action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    
    db.commit()
    return post_query.first()