from fastapi import FastAPI
from src.routes.articles import articles_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Welcome to my Personal Blogging Platform API"}

app.include_router(
    router = articles_router,
    prefix = "/api/v1/articles",
    tags = ["v1"]
)