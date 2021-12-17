from .. import schemas, utils
from ..database import get_session
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, APIRouter
import psycopg2

router = APIRouter(
    prefix = "/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts():
    conn = get_session()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()
        return posts
    return Response(status_code=status.HTTP_404_NOT_FOUND) 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate):
    conn = get_session()
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", (post.title, post.content, post.published))
        new_post = cursor.fetchone()
    conn.commit()
    return new_post

@router.get("/{id}",response_model=schemas.PostResponse)
def get_post(id: int):
    conn = get_session()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM posts WHERE id=%s", str(id))
        post = cursor.fetchone()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    return post
    

@router.delete("/{id}")
def delete_post(id: int):
    conn = get_session()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM posts WHERE id=%s RETURNING *", str(id))
        deleted_post = cursor.fetchone()
        if not deleted_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    conn.commit()
    # return {"data": deleted_post}
    return Response(status_code=status.HTTP_204_NO_CONTENT) 

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate):
    conn = get_session()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE posts SET title=%s, content=%s, published=%s WHERE id=%s RETURNING *", (post.title, post.content, post.published, str(id)))
        updated_post = cursor.fetchone()
        if updated_post == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    conn.commit()
    
    return updated_post
