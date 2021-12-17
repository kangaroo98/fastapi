from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor

from .routers import posts, users 

from random import randrange
import time


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Hello World "}
    
