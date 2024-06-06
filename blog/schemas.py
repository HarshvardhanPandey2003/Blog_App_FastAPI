from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
@app.post('/blog')
def index():
    return {"data": "All blogs here"}

