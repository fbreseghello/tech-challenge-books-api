import pandas as pd

def load_books_data():
    df = pd.read_csv("data/books.csv")
    df["id"] = df.index  # Adiciona uma coluna ID numérica baseada no índice
    return df

