from fastapi import FastAPI, Depends, HTTPException, status
from database import Base, engine, SessionLocal



from routers import user
from routers import login
app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(login.router)
app.include_router(user.router)



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Blog CRUD Operations
# @app.get('/blog', tags=['Blogs'], response_model=list[schemas.ShowBlogs])
# def get_all_blogs(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

# @app.post('/blog', tags=['Blogs'], status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlogs)
# def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
#     new_blog = models.Blog(
#         title=request.title, 
#         body=request.body, 
#         published=request.published,
#         user_id=2  # You should replace this with actual user authentication
#     )
#     db.add(new_blog)
#     db.commit()
#     db.refresh(new_blog)
#     return new_blog

# @app.get('/blog/{id}', tags=['Blogs'], response_model=schemas.ShowBlogs)
# def get_blog(id: int, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id).first()
#     if not blog:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
#     return blog

# @app.put('/blog/{id}', tags=['Blogs'], response_model=schemas.ShowBlogs)
# def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
#     blog.update({
#         'title': request.title,
#         'body': request.body,
#         'published': request.published
#     })
#     db.commit()
#     return blog.first()

# @app.delete('/blog/{id}', tags=['Blogs'])
# def delete_blog(id: int, db: Session = Depends(get_db)):
#     blog = db.query(models.Blog).filter(models.Blog.id == id)
#     if not blog.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
#     blog.delete(synchronize_session=False)
#     db.commit()
#     return {"detail": "Blog deleted successfully"}

# # User CRUD Operations
# @app.post('/user', tags=['Users'], status_code=status.HTTP_201_CREATED, response_model=schemas.ShowUser)
# def create_user(request: schemas.User, db: Session = Depends(get_db)):
#     new_user = models.User(
#         name=request.name,
#         email=request.email,
#         password=HashPassword.bcrypt(request.password)  # Hash the password
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user

# @app.get('/user', tags=['Users'], response_model=list[schemas.ShowUser])
# def get_all_users(db: Session = Depends(get_db)):
#     users = db.query(models.User).all()
#     return users

# @app.get('/user/{id}', tags=['Users'], response_model=schemas.ShowUser)
# def get_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
#     return user

# @app.put('/user/{id}', tags=['Users'], response_model=schemas.ShowUser)
# def update_user(id: int, request: schemas.User, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id)
#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
#     user.update({
#         'name': request.name,
#         'email': request.email,
#         'password': HashPassword.bcrypt(request.password)  # Hash the password
#     })
#     db.commit()
#     return user.first()

# @app.delete('/user/{id}', tags=['Users'])
# def delete_user(id: int, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.id == id)
#     if not user.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    
#     user.delete(synchronize_session=False)
#     db.commit()
#     return {"detail": "User deleted successfully"}