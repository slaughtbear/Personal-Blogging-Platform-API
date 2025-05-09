from fastapi import APIRouter, HTTPException
from src.schemas.articles import Article
from src.database.config import supabase

articles_router = APIRouter()

@articles_router.get("/")
def get_all_articles() -> list[Article]:
    """
    Endpoint de tipo GET para obtener todas las publicaciones
    en la base de datos

    returns:
        list[Article]: Lista con todas las publicaciones
    """
    articles = supabase.table("articles").select("*").execute()
    if not articles.data:
        raise HTTPException(
            status_code = 404,
            detail = "No se encontró ninguna publicación creada en la base de datos"
        )
    return articles.data