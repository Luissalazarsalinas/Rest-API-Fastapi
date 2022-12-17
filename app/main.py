from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from app.routers import post, users, auth, vote

## Connection to create all tables 
#models.Base.metadata.create_all(bind=engine)

## Create a instance of the app
app = FastAPI()

# # home path 
# @app.get("/")
# def root():
#     return {"Message": "Wolcome to init page"}

# Origin 
# * allows request from whatever domains
# for more secure practice is to better specify the differenst domains for your api
origins = ["*"]

# ADD CORS (Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add to routers
app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
