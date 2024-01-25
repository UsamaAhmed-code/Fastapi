from typing import List
from fastapi import Depends, FastAPI, HTTPException, Response, status
from pydantic import BaseModel
from . import models, schemas, utils
from .database import engine, get_db
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .utils import hash
from .routers import post, user, auth

models.Base.metadata.create_all(bind = engine)


app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)