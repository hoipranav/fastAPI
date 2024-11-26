from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time
from sqlalchemy.orm import Session 
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv('host'), 
            database=os.getenv('database'), 
            user=os.getenv('user'), 
            password=os.getenv('password'),
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
        print('Database connection was succesful')
        break
    except Exception as error:
        print('Connection to the Database failed')
        print("Error: ", error)
        time.sleep(5) 
 
    
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

def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i

@app.get('/')
async def home():
    return {"message": "Welcome to our API"}


@app.get('/sqlalchemy')
def test_post(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post)
    print(posts)
    return {"data": "Success"}


@app.get('/posts')
async def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
    posts = db.query(models.Post).all()
    return {"message": posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
async def create_posts(post: Post, db: Session = Depends(get_db)):
    # cursor.execute(""" 
    #                INSERT INTO posts 
    #                (title, content, published) 
    #                VALUES (%s, %s, %s) RETURNING * """, 
    #                (post.title, post.content, post.published)
    #     )
    # new_post = cursor.fetchone()
    # conn.commit()
    
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}  


@app.get('/posts/{id}')
async def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} was not found")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put('/posts/{id}')
async def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {id} does not exist")
    return {"data": updated_post}