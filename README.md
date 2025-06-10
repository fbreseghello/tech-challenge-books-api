# Tech Challenge - Books API

Este projeto consiste na construção de uma API pública para consulta de livros extraídos via Web Scraping do site [Books to Scrape](https://books.toscrape.com/).

## Features

- Web Scraping automatizado dos livros.
- API RESTful desenvolvida com FastAPI.
- Deploy público para fácil consumo da API.
- Endpoints de busca, detalhes, categorias e estatísticas.

## Instalação

Clone o repositório e instale as dependências:
```bash
git clone https://github.com/seuusuario/tech-challenge-books-api.git
cd tech-challenge-books-api
pip install -r requirements.txt
```

## Execução

Para rodar a API localmente:
```bash
uvicorn api.main:app --reload
```

## Endpoints

- `GET /api/v1/books`
- `GET /api/v1/books/{id}`
- `GET /api/v1/books/search?title={title}&category={category}`
- `GET /api/v1/categories`
- `GET /api/v1/health`

(Detalhes completos da documentação via Swagger: `/docs`)
