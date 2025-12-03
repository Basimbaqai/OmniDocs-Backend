from fastapi import FastAPI
from routers import user, login, document
from database import engine
import models
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(login.router)
app.include_router(user.router)

app.include_router(document.router)


@app.get("/")
def root():
    return {"message": "Welcome to OmniDocs API"}
