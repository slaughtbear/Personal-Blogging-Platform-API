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

@articles_router.get("/{id}")
def get_one_article(id: int) -> Article:
    """
    Endpoint de tipo GET para obtener una publicación buscando
    por id en la base de datos

    returns:
        Article: Publicación
    """
    article = search_article(id)
    if not article:
        raise HTTPException(
            status_code = 404,
            detail = "No se encontró ninguna publicación creada en la base de datos"
        )
    return article
    
def search_article(id: int) -> dict | None:
    """
    Función auxiliar para buscar una publicación por id en la base de datos

    returns:
        dict: Publicación si se encuentra
        None: Si la publicación no existe
    """
    article = supabase.table("articles").select("*").eq("id", id).execute()
    return article.data[0] if article.data else None