from fastapi import FastAPI

app = FastAPI()


# Request Guest method url: "/"

@app.get("/")
async def root():
    return {"message": "Welcome to my API!!!!"}


@app.get("/posts")
def get_posts():
    return {"data": "This is your posts."}
