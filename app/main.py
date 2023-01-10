from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import models
from database import engine
from routers import post, user, auth, vote
from config import Settings

#-----------------| ORM CREATING CONNECTION BETWEEN DB AND MODELS|----------------------
#models.Base.metadata.create_all(bind=engine)
# alembic is making the table for us

#-----------------| APP |----------------------
app = FastAPI()

origins = ['*'] # sites that can call api requests

# before requests the app goes through the middelware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True, 
    allow_methods=["*"],    # request methods that are allowed. now its all methods(for eg. for public api u may only want to allow GET requests)
    allow_headers=["*"],    # request headers that are allowed
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

#-----------------| ROOT |----------------------
@app.get('/')
def root():
    return {'message': 'Welcome to my API'}

