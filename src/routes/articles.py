from datetime import date
from fastapi import APIRouter, HTTPException
from src.schemas.articles import Article, ArticleCreate, ArticleUpdate
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

@articles_router.post("/", status_code = 201)
def create_article(article_data: ArticleCreate) -> Article:
    if search_article_by_title(article_data.title):
        raise HTTPException(
            status_code = 409,
            detail = "La publicación que estás intentando crear ya existe"
        )
    new_article = supabase.table("articles").insert({
        "published_at": date.today().isoformat(),
        "title": article_data.title,
        "content": article_data.content,
        "tags": article_data.tags
    }).execute()
    return new_article.data[0]

@articles_router.put("/{id}")
def update_article(id: int, article_data: ArticleUpdate) -> Article:
    stored_article = search_article(id)
    if not stored_article:
        raise HTTPException(
                status_code = 404,
                detail = "La publicación que estás intentando actualizar no existe"
            )
    
    updated_article = (
            supabase.table("articles")
            .update(article_data.model_dump())
            .eq("id", id)
            .execute()
        )
    return updated_article.data[0]

@articles_router.delete("/{id}")
def delete_article(id: int) -> dict:
    stored_article = search_article(id)
    if not stored_article:
        raise HTTPException(
                status_code = 404,
                detail = "La publicación que estás intentando eliminar no existe"
            )
    
    supabase.table("articles").delete().eq("id", id).execute()
    return {"msg": "Publicación eliminada correctamente"}

@articles_router.patch("/{id}")
def partial_update_article(id: int, article_data: ArticleUpdate) -> Article:
    stored_article = search_article(id)
    if not stored_article:
        raise HTTPException(
                status_code = 404,
                detail = "La publicación que estás intentando actualizar no existe"
            )
    
    updated_article = (
            supabase.table("articles")
            .update(article_data.model_dump(exclude_unset = True))
            .eq("id", id)
            .execute()
        )
    return updated_article.data[0]
    
def search_article(id: int) -> dict | None:
    """
    Función auxiliar para buscar una publicación por id en la base de datos

    returns:
        dict: Publicación si se encuentra
        None: Si la publicación no existe
    """
    article = supabase.table("articles").select("*").eq("id", id).execute()
    return article.data[0] if article.data else None

def search_article_by_title(title: str):
    """
    Función auxiliar para buscar una publicación por título en la base de datos

    returns:
        dict: Publicación si se encuentra
        None: Si la publicación no existe
    """
    article = supabase.table("articles").select("*").eq("title", title).execute()
    return article.data[0] if article.data else None