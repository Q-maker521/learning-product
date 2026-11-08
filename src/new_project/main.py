from typing import Optional

from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


my_pots = [{"title": "First Post", "content": "This is the content of the first post", "id": 1},
           {"title": "Second Post", "content": "This is the content of the second post", "id": 2},]

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/")
async def login_user():
    return {"message": "Hello World"}

@app.get("/posts")
async def get_posts():
    return {"message": my_pots}

@app.post("/posts")
async def create_posts(Post:Post):
    post_dict = Post.model_dump(exclude_unset=True)
    post_dict["id"] = len(my_pots) + 1
    my_pots.append(post_dict)
    return {"data": post_dict}