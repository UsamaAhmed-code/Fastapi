from typing import List
from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    tags=['Users']
)

@router.post("/user/create", response_model=schemas.UserOut)
def CreateUser(user: schemas.UserCreate, db: Session= Depends(get_db)):

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    create_user = models.User(**user.dict())
    db.add(create_user )
    db.commit()
    db.refresh(create_user)
    return create_user



@router.get("/get/oneuser/{id}", response_model= schemas.UserOut)
def get_one(id: int , db: Session=Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id )

    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the user with id : {id} not found")
    return user.first()

    