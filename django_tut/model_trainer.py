import sqlite3
import pandas as pd
import pickle
from books import models
from sklearn.metrics.pairwise import cosine_similarity

connection = sqlite3.connect("db.sqlite3")

book_query = "select * from books_book;"
reader_query = "select * from books_customer;"
book_rating_query = "select * from books_rating;"

book_df = pd.read_sql(book_query, connection)
reader_df = pd.read_sql(reader_query, connection)
book_rating_df = pd.read_sql(book_rating_query, connection)


def popular_books(push_to_db=False):
    num_rating_df = book_rating_df.groupby("book_id").count()[
        "rating"].reset_index()
    num_rating_df.rename(columns={"rating": "num_ratings"}, inplace=True)

    avg_rating_df = book_rating_df.groupby("book_id").mean()[
        "rating"].reset_index()
    avg_rating_df.rename(columns={"rating": "avg_rating"}, inplace=True)

    popular_df = num_rating_df.merge(avg_rating_df, on='book_id')
    book_ids = popular_df[popular_df.num_ratings >= 70].sort_values(
        'avg_rating', ascending=False).head(50).book_id

    print(book_df[book_df.id.isin(book_ids)][['id', 'title']])

    popular_books = models.Book.objects.filter(id__in=book_ids)

    if push_to_db:
        books_to_store = [models.PopularBooks(
            book=book) for book in popular_books]
        models.PopularBooks.objects.bulk_create(books_to_store)


def collaborative_filtering():
    group_rating_by_reader = book_rating_df.groupby(
        'customer_id').count()['rating'] >= 125
    readers_to_consider = group_rating_by_reader[group_rating_by_reader].index

    filtered_ratings = book_rating_df[book_rating_df.customer_id.isin(
        readers_to_consider)]

    group_rating_by_book = book_rating_df.groupby('book_id').count()[
        'rating'] >= 100
    books_to_consider = group_rating_by_book[group_rating_by_book].index

    final_ratings = filtered_ratings[filtered_ratings.book_id.isin(
        books_to_consider)]

    pivot_table = final_ratings.pivot_table(
        index='book_id', columns='customer_id', values='rating')
    pivot_table.fillna(0, inplace=True)

    similarity_scores = cosine_similarity(pivot_table)
    pickle.dump(pivot_table, open('pivot_table.pkl', 'wb'))
    pickle.dump(similarity_scores, open('similarity_score.pkl', 'wb'))


collaborative_filtering()
