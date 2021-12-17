from time import time
from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published : bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int




class UserBase(BaseModel):
    email: EmailStr
    
class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int