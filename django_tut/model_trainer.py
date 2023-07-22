import sqlite3
import pandas as pd

connection = sqlite3.connect("db.sqlite3")

book_query = "select * from books_book;"
reader_query = "select * from books_customer;"
book_rating_query = "select * from books_rating;"

book_df = pd.read_sql(book_query, connection)
reader_df = pd.read_sql(reader_query, connection)
book_rating_df = pd.read_sql(book_rating_query, connection)


def popular_books():
    num_rating_df = book_rating_df.groupby("book_id").count()[
        "rating"].reset_index()
    num_rating_df.rename(columns={"rating": "num_ratings"}, inplace=True)

    avg_rating_df = book_rating_df.groupby("book_id").mean()[
        "rating"].reset_index()
    avg_rating_df.rename(columns={"rating": "avg_rating"}, inplace=True)

    popular_df = num_rating_df.merge(avg_rating_df, on='book_id')
    book_ids = popular_df[popular_df.num_ratings >= 70].sort_values(
        'avg_rating', ascending=False).head(50).book_id

    popular_df = book_df[book_df.id.isin(book_ids)]
