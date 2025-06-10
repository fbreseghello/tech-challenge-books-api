# Tech Challenge - Books API

API pública de consulta de livros extraídos via Web Scraping de [books.toscrape.com](https://books.toscrape.com/), pronta para integrações com Data Science e Machine Learning.

## Features

- Web Scraping automatizado de 1000 livros (título, preço, rating, disponibilidade, categoria, imagem)
- API RESTful completa, documentada e pronta para produção
- Filtros por título, categoria, faixa de preço, livros top-rated, estatísticas e mais
- Deploy simples em nuvem (Heroku, Render, etc)
- Arquitetura modular para escalabilidade futura

## Endpoints principais

| Método | Endpoint                              | Descrição                            |
|--------|---------------------------------------|--------------------------------------|
| GET    | /api/v1/books                        | Lista todos os livros                |
| GET    | /api/v1/books/{id}                   | Detalhe de um livro pelo id          |
| GET    | /api/v1/books/search?title=&category=| Busca por título e/ou categoria      |
| GET    | /api/v1/books/top-rated?limit=10     | Lista os livros com melhor avaliação |
| GET    | /api/v1/books/price-range?min=&max=  | Lista livros por faixa de preço      |
| GET    | /api/v1/categories                   | Lista todas as categorias            |
| GET    | /api/v1/stats/overview               | Estatísticas gerais da coleção       |
| GET    | /api/v1/stats/categories             | Estatísticas por categoria           |
| GET    | /api/v1/health                       | Status e integridade da API          |

## Como rodar local

```bash
git clone https://github.com/seunome/tech-challenge-books-api.git
cd tech-challenge-books-api
python -m venv .venv
source .venv/bin/activate  # Ou .venv\Scripts\activate no Windows
pip install -r requirements.txt
python scripts/scraping.py      # Só precisa rodar 1x para criar o books.csv
uvicorn api.main:app --reload
