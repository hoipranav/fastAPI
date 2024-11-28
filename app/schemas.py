from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    
    class Condig:
        orm_mode = True