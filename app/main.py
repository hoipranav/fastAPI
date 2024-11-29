from fastapi import FastAPI
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import time
from . import models
from .database import engine
from .routers import posts, users, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get('/')
async def home():
    return {"message": "Welcome to our API"}