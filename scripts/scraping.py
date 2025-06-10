import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://books.toscrape.com/"
START_URL = BASE_URL + "catalogue/page-1.html"

def get_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")

def get_book_info(book_tag):
    title = book_tag.h3.a["title"]
    relative_url = book_tag.h3.a["href"]
    book_url = BASE_URL + "catalogue/" + relative_url

    price = book_tag.select_one(".price_color").text.strip()
    availability = book_tag.select_one(".availability").text.strip()
    rating_tag = book_tag.select_one("p.star-rating")
    rating = rating_tag["class"][1] if rating_tag else "No rating"

    book_soup = get_soup(book_url)
    category = book_soup.select("ul.breadcrumb li a")[-1].text.strip()
    image_url = BASE_URL + book_soup.select_one(".carousel-inner img")["src"].replace("../", "")

    return {
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating,
        "category": category,
        "image_url": image_url
    }

def scrape_books():
    books_data = []
    page = 1

    while True:
        url = BASE_URL + f"catalogue/page-{page}.html"
        print(f"Scraping page {page}...")

        try:
            soup = get_soup(url)
        except requests.exceptions.HTTPError as e:
            print(f"Página {page} não encontrada. Scraping finalizado.")
            break

        books = soup.select("article.product_pod")
        if not books:
            break

        for book_tag in books:
            try:
                info = get_book_info(book_tag)
                books_data.append(info)
            except Exception as e:
                print(f"Erro ao processar livro: {e}")

        page += 1
        time.sleep(1)

    df = pd.DataFrame(books_data)
    df.to_csv("data/books.csv", index=False)
    print(f"Scraping finalizado com sucesso! {len(books_data)} livros salvos.")

if __name__ == "__main__":
    scrape_books()
