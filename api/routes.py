from fastapi import APIRouter, HTTPException
from api.models import Book
from api.database import load_books_data
from fastapi import Query

router = APIRouter(prefix="/api/v1")

@router.get("/books", response_model=list[Book])
def get_all_books():
    df = load_books_data()
    books = df.to_dict(orient="records")
    return books

@router.get("/books/search", response_model=list[Book])
def search_books(title: str = Query(None), category: str = Query(None)):
    df = load_books_data()
    # Filtrando por título, se fornecido
    if title:
        df = df[df["title"].str.contains(title, case=False, na=False)]
    # Filtrando por categoria, se fornecido
    if category:
        df = df[df["category"].str.contains(category, case=False, na=False)]
    books = df.to_dict(orient="records")
    return books

@router.get("/books/{id}", response_model=Book)
def get_book_by_id(id: int):
    df = load_books_data()
    if id < 0 or id >= len(df):
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    book = df.iloc[id].to_dict()
    return book

@router.get("/categories", response_model=list[str])
def get_categories():
    df = load_books_data()
    categories = sorted(df["category"].unique())
    return categories

@router.get("/health")
def healthcheck():
    try:
        df = load_books_data()
        total = len(df)
        return {"status": "ok", "books_count": total}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
