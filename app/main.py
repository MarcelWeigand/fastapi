# this version is using sqlalchemy to write python code that communicates with the database instead of sql commands
# Tabelle in postgres wird direkt über python erstellt und nicht über pgadmin


from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote #
from .config import settings
from fastapi.middleware.cors import CORSMiddleware



print(settings.database_hostname)

models.Base.metadata.create_all(bind=engine) # create all of the models

app = FastAPI()


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all() # to access the model which represents a table, db.query is transforming it into a SQL command
#     return {"data": posts}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}

# @app.get("/posts", response_model=List[schemas.Post])
# def get_posts(db: Session = Depends(get_db)):
#     posts = db.query(models.Post).all()
#     return posts


# @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
# def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db)): #post is stored in the Post object
#     # new_post = models.Post(**post.dict())  # put all columns in a dict and unpack it so that you dont have to code every column
#     new_post = models.Post(title=post.title, content=post.content, published=post.published)
#     db.add(new_post)
#     db.commit()
#     db.refresh(new_post)
#     return new_post


# @app.get("/posts/{id}", response_model=schemas.Post) #id is a path parameter
# def get_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id).first()
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with id: {id} was not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": f"post with ih: {id} was not found"}
#     return post


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int, db: Session = Depends(get_db)):
#     post = db.query(models.Post).filter(models.Post.id == id)

#     if post.first() == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id: {id} does not exist")
    
#     post.delete(synchronize_session=False)
#     db.commit()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)


# @app.put("/posts/{id}", response_model=schemas.Post)
# def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db)):
#     post_query = db.query(models.Post).filter(models.Post.id == id)
#     post = post_query.first()

#     if post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post with id: {id} does not exist")
#     # post_query.update({'title': 'my updated title', 'content': 'my updated content'}, synchronize_session=False)
#     post_query.update(updated_post.dict(), synchronize_session=False)
    
#     db.commit()
#     return post_query.first()



# @app.post("/users", status_code=status.HTTP_201_CREATED,  response_model=schemas.UserOut)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

#     # hash the pw from user.password
#     hashed_password = utils.hash(user.password)
#     user.password = hashed_password

#     new_user = models.User(**user.dict())
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return new_user

# @app.get('/users/{id}',  response_model=schemas.UserOut)
# def get_user(id: int, db: Session = Depends(get_db)):

#     user = db.query(models.User).filter(models.User.id == id).first()

#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} doe not exist")
    
#     return user