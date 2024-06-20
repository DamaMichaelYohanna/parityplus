import os
import pathlib

from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlmodel import SQLModel, Session

from insight.routing import insight
from user.views import user
from crime.routing import crime
from job.routing import job
from database import engine


app = FastAPI()
app.mount('/crime', crime)
app.mount('/insight', insight)
app.mount('/job', job)
app.mount('/user', user)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
# Base class for database models

# This will create the database tables
SQLModel.metadata.create_all(bind=engine)