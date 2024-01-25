from typing import List

from app import oauth2
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router  = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_post(db: Session = Depends(get_db) ):
   
    post = db.query(models.Post).all() 
    return  post


@router.post("/create", response_model=schemas.PostResponse)
def create_post(post: schemas.Post, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id = get_current_user.id , **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return  new_post

@router.get("/onepost/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db) ):

    one_post = db.query(models.Post).filter(models.Post.id == id ).first()
    if not one_post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id : {id} not found")
    return one_post
@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT )
def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id : {id} not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/update/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user) ):

    updated_post = db.query(models.Post).filter(models.Post.id == id)
    newpost = updated_post.first()

    if newpost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post with id : {id} not found")
    
    updated_post.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post.first()
