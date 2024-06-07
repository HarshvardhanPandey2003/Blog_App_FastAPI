from fastapi import FastAPI,Depends, Response,status
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session 
app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog",status_code=201)
def create(request: schemas.Blog,db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog")
def all(db:Session = Depends(get_db)):
    return db.query(models.Blog).all()

@app.get("/blog/{id}",status_code=200)
def show(id,response:Response, db:Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f'Blog with the id {id} not found'}
    return blog

@app.delete("/blog/{id}", status_code=204)
def delete_blog(id: int,response:Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog with the id {id} not found"}

    db.delete(blog)
    db.commit()

    remaining_blogs = db.query(models.Blog).all()
    return {"message": f"Blog with id {id} has been deleted", "remaining_blogs": remaining_blogs}