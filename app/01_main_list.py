# from fastapi import FastAPI, Response, status, HTTPException
# from fastapi.params import Body
# from typing import Optional
# from pydantic import BaseModel
# from random import randrange

# app = FastAPI()


# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True # if user not provides the field its set to True
#     rating: Optional[int] = None # if it's not set it's completely optional




# my_posts = [{"title": "title1", "content": "content1", "id": 1},
# {"title": "food", "content": "food is great", "id": 2}]

# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i





# @app.get("/")
# def root():
#     return {"message": "Hello World"}

# @app.get("/posts")
# def get_posts():
#     return {"data": my_posts}

# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# # extract body from the payload, transform it into a dictionary and save it into payload variable
# def create_posts(post: Post):
#     #print(post.title)
#     #print(post.dict()) # converts the pydantic model into a dict
#     post_dict = post.dict()
#     post_dict['id'] = randrange(0,100000)
#     my_posts.append(post_dict)
#     return {"data": post_dict}

# @app.get("/posts/{id}") #id is a path parameter
# def get_post(id: int, response: Response):
#     post = find_post(int(id))
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"post with ih: {id} was not found"}
#     return {"post_detail": post}


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     index = find_index_post(id)

#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id: {id} does not exist")
#     my_posts.pop(index)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id: int, post:Post):
#     index = find_index_post(id)
#     if index == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id: {id} does not exist")
#     post_dict = post.dict()
#     post_dict['id'] = id
#     my_posts[index] = post_dict
#     return {"data": post_dict}
