from fastapi import FastAPI,Depends, Response,status
from . import schemas,models,hashing
from .database import engine,SessionLocal,SessionLocal2
from sqlalchemy.orm import Session 
app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def get_db2():
#     db = SessionLocal2()
#     try:
#         yield db
#     finally:
#         db.close()

@app.post("/blog",status_code=201,tags=["blogs"])
def create(request: schemas.Blog,db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog",tags=["blogs"])
def all(db:Session = Depends(get_db)):
    return db.query(models.Blog).all()

@app.get("/blog/{id}",status_code=200,response_model=schemas.ShowBlog,tags=["blogs"])
def show(id,response:Response, db:Session = Depends(get_db)):
    blog=db.query(models.Blog).filter(models.Blog.id==id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f'Blog with the id {id} not found'}
    return blog

@app.delete("/blog/{id}", status_code=204,tags=["blogs"])
def delete_blog(id: int,response:Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {"detail": f"Blog with the id {id} not found"}

    db.delete(blog)
    db.commit()

    remaining_blogs = db.query(models.Blog).all()
    return {"message": f"Blog with id {id} has been deleted", "remaining_blogs": remaining_blogs}


@app.post('/user',tags=["user"])
def create_user(request: schemas.User, db: Session = Depends(get_db2)):
    new_user = models.User(name=request.name, email=request.email,password=hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/user/{id}",status_code=200,response_model=schemas.ShowUser,tags=["user"])
def show(id,response:Response, db:Session = Depends(get_db2)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'detail': f'User with the id- {id} not found'}
    return user