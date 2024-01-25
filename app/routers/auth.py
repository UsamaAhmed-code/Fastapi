from fastapi import APIRouter, FastAPI, HTTPException, Response, Depends, status
from sqlalchemy.orm import Session

from app import models, utils
from .. import database, schemas, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=['Authntication'])

@router.post('/login')
def login(user_credentails: OAuth2PasswordRequestForm = Depends() ,  db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentails.username ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f"Invaild Credentilas")
    
    if not utils.verify(user_credentails.password, user.password):
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, details = f"Invaild Credentails")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id}) 
    return {"access_token": access_token, "token_type": "bearer"} 