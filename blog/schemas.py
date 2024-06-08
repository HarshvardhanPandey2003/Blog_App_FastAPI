# Here we define structure of a class that we're going to use 
from fastapi import FastAPI
from pydantic import BaseModel


class Blog(BaseModel):
    title:str
    body:str

# Extending Blog Class
class ShowBlog(BaseModel):
    title: str
    class Config():
        from_attributes = True

class User(BaseModel):
    name:str
    email:str
    password:str

class ShowUser(BaseModel):
    name:str
    email:str
    class Config():
        from_attributes = True