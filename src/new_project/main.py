from typing import Optional

from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from itertools import count



my_posts = [{"title": "First Post", "content": "This is the content of the first post", "id": 1},
           {"title": "Second Post", "content": "This is the content of the second post", "id": 2},]

post_ids = count(
    start=max((post["id"] for post in my_posts), default=0) + 1
)

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
    return {"message": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(Post:Post):
    post_dict = Post.model_dump(exclude_unset=True)
    post_dict["id"] = next(post_ids)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{post_id}")
async def get_post(post_id: int, response: Response):
    for post in my_posts:
        if post["id"] == post_id:
            return {"data": post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.delete("/posts/delete/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int):
    for post in my_posts:
        if post["id"] == post_id:
            my_posts.remove(post)
            return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.put("/posts/{post_id}")
async def update_post(post_id:int,post:Post):
    for existing_post in my_posts:
        if existing_post["id"] == post_id:
            existing_post.update(post.model_dump(exclude_unset=True))
            return {"data": existing_post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
