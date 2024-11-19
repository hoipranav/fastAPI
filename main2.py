from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
    
    
my_posts = [
    {
        "title": "Beaches in Florida",
        "content": "Braches are just great",
        "id": 1
    },
    {
        "title": "Favourite foods",
        "content": "I like pizza",
        "id": 2
    }
]    


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


@app.get('/')
async def home():
    return {"message": "Welcome to our API"}


@app.get('/posts')
async def get_posts():
    return {"message": my_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data": post_dict}  


@app.get('/posts/{id}')
async def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} was not found")
    return {"data": post}