# this version is using a database instead of an array

from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True # if user not provides the field its set to True
    rating: Optional[int] = None # if it's not set it's completely optional

while True:
    try:
        conn = psycopg2.connect(host = 'localhost',
                                database = 'fastapi', #database name in postgres
                                user = 'postgres', #default postgres username
                                password = 'Bayernamas1900?',
                                cursor_factory=RealDictCursor #give column names as well
                                )
        cursor = conn.cursor()
        print("DB connection suc")
        break
    except Exception as error:
        print("Connection failed")
        print("Error: ", error)
        time.sleep(2)


my_posts = [{"title": "title1", "content": "content1", "id": 1},
{"title": "food", "content": "food is great", "id": 2}]



def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i





@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
# extract body from the payload, transform it into a dictionary and save it into payload variable
def create_posts(post: Post):
    # cursor.execute(f"INSERT INTO post (title, content, published) VALUES({post.title}, {post.content})") # this is not recommended as it can cause SQL injection
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published)) # parameterize all the data that we put into swl statement 
    new_post = cursor.fetchone() # to get the result from returning statement
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}") #id is a path parameter
def get_post(id: int):
    cursor.execute(""" SELECT * from posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with ih: {id} was not found"}
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE from posts WHERE id = %s returning * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id: {id} does not exist")
    

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post:Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning*  """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id: {id} does not exist")
    
    return {"data": updated_post}