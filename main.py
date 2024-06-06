from fastapi import FastAPI
from typing import Optional
app = FastAPI()

@app.get('/') 
def index():
    return {"Data": "Blog List"}

@app.get('/blog')
def show(limit=10, published : bool=True, sort : Optional[str] = None):
    #Example of Default Parameter and Optional parameter,
    if published==True:
        return {'data': f'{limit} are the published blogs from db'}
    else:
        return {'data': f'{limit} are the blogs from db'}

#id is a path parameter 
@app.get('/blog/{id}')
def show(id:int):
    return {'data': id}

@app.get('/blog/{id}/Unpublished')
def Unpublished():
    return {'data': {"Blogs":"Unpublished"} }

@app.post('/Blog') 
def index():
    return {"Data": "The Blog is Created "}
