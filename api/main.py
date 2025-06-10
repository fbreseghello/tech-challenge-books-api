from fastapi import FastAPI
from api.routes import router  # <-- Importando o router com os endpoints

app = FastAPI(
    title="Books API",
    version="1.0.0",
    description="API pública para consulta de livros extraídos de Books to Scrape."
)

app.include_router(router)  # <-- Isso aqui é ESSENCIAL
