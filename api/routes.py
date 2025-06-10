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

@router.get("/books/top-rated", response_model=list[Book])
def get_top_rated_books(limit: int = 10):
    df = load_books_data()
    # Considera "Five" como nota máxima
    top_books = df[df["rating"] == "Five"].head(limit)
    books = top_books.to_dict(orient="records")
    return books

@router.get("/books/price-range", response_model=list[Book])
def books_in_price_range(
    min: float = Query(..., description="Preço mínimo"),
    max: float = Query(..., description="Preço máximo")
):
    df = load_books_data()
    df["price_num"] = df["price"].str.replace("Â£", "").str.replace("£", "").astype(float)
    filtered = df[(df["price_num"] >= min) & (df["price_num"] <= max)]
    books = filtered.to_dict(orient="records")
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

@router.get("/stats/overview")
def stats_overview():
    df = load_books_data()
    
    # Limpa o símbolo de libra e converte para float
    df["price_num"] = df["price"].str.replace("Â£", "").str.replace("£", "").astype(float)
    
    total_books = len(df)
    avg_price = round(df["price_num"].mean(), 2)
    rating_dist = df["rating"].value_counts().to_dict()
    
    return {
        "total_books": total_books,
        "average_price": avg_price,
        "rating_distribution": rating_dist
    }

@router.get("/stats/categories")
def stats_by_category():
    df = load_books_data()
    # Limpa e converte o preço
    df["price_num"] = df["price"].str.replace("Â£", "").str.replace("£", "").astype(float)
    # Agrupa por categoria
    stats = (
        df.groupby("category")
        .agg(
            total_books=("id", "count"),
            average_price=("price_num", "mean")
        )
        .reset_index()
    )
    # Arredonda o preço médio
    stats["average_price"] = stats["average_price"].round(2)
    # Transforma em lista de dicts
    return stats.to_dict(orient="records")