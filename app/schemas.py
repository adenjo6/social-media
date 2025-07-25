from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

from pydantic.types import conint

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(UserBase):
    pass
    
class Token(BaseModel): 
    access_token: str
    token_type: str
 
class TokenData(BaseModel):
    id: Optional[int] = None

class PostBase(BaseModel): 
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int  
    created_at: datetime
    owner_id: int
    owner: UserOut

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True

    class Config:
        orm_mode = True
class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)

 