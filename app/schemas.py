from datetime import datetime
from typing import Annotated
from pydantic import EmailStr, BaseModel, Field
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str=Field(..., min_length=8, max_length=72)
class UserCreate(BaseModel):
    email: EmailStr
    password: str=Field(..., min_length=8, max_length=72)  
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id:int
    owner_id:int
    owner:UserOut
    class Config:
        orm_mode=True

    
  



class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id: str | None = None

class Vote(BaseModel):
    post_id:int
    dir: Annotated[int, Field(le=1)]
class PostOut(BaseModel):
    Post: PostResponse
    votes:int

    class Config:
        orm_mode=True