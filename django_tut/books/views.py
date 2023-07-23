import random
import numpy as np
import pandas as pd
from django.shortcuts import render
from . import models


pivot_table = pd.read_pickle("pivot_table.pkl")
similarity_scores = pd.read_pickle("similarity_score.pkl")


def index(request):
    books = get_popular_books()
    return render(request, 'books/index.html', context={
        'best_sellers': books,
        'user': {
            'firstname': "Mahfuzur Rahman"
        }
        # 'user': None,
    })


def book_detail(request, id: int):
    book = models.Book.objects.get(id=id)
    similar_books = recommend_book(book.id)

    return render(request, 'books/book_detail.html', context={
        'book': book,
        'recommendation': similar_books,
        'user': {
            'firstname': 'Mahfuzur Rahman'
        }
    })


def book_suprise(request):
    book_title = request.GET.get('book-title')

    if book_title:
        book_id = models.Book.objects.get(title=book_title).id
        surprise_books = recommend_book(book_id, 20)

        return render(request, 'books/surprise.html', {
            'book_title': book_title,
            'similar_books': surprise_books
        })

    return render(request, 'books/surprise.html')


def recommend_book(book_id: int, count: int = 5):
    index_array = np.where(pivot_table.index == book_id)[0]
    if index_array.shape[0] == 0:
        return get_popular_books(5)
    index = index_array[0]
    similar_items = sorted(list(
        enumerate(similarity_scores[index])), key=lambda item: item[1], reverse=True)[1:1+count]

    similar_book_ids = [pivot_table.index[item[0]] for item in similar_items]

    return models.Book.objects.filter(id__in=similar_book_ids)


def get_popular_books(count: int = None):
    popular_books = [
        popular_book.book for popular_book in models.PopularBooks.objects.all()]
    random.shuffle(popular_books)
    if count:
        return popular_books[:count]
    return popular_books
