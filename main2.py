from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get('/')
async def home():
    return {"message": "Welcome to our API"}


@app.get('/posts')
async def get_posts():
    return {"message": "This is the post method"}


@app.post('/createposts')
async def create_posts(post: Post):
    print(post)
    print(post.model_dump())
    return {"data": post.model_dump()}