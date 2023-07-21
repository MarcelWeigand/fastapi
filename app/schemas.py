from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

# pydantic model, schema
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # if user not provides the field its set to True
    #rating: Optional[int] = None # if it's not set it's completely optional



class UserCreate(BaseModel):
    email: EmailStr
    password: str

# response schema
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostCreate(PostBase):
    pass

# response model
class Post(PostBase):
    id: int
    # title: str
    # content: str
    # published: bool
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True