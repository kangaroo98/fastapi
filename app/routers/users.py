from .. import schemas, utils
from ..database import get_session
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, APIRouter


router = APIRouter(
    prefix = "/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate):
    conn = get_session()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *", (user.email, utils.hash(user.password)))
            new_post = cursor.fetchone()
        conn.commit()
    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user was not created: {error}")
    
    return new_post

@router.get("/{id}",response_model=schemas.UserResponse)
def get_user(id: int):
    conn = get_session()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE id=%s", str(id))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return user
