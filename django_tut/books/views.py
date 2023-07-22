import numpy as np
import pandas as pd
from django.shortcuts import render
from . import models


pivot_table = pd.read_pickle("pivot_table.pkl")
similarity_scores = pd.read_pickle("similarity_score.pkl")


def index(request):
    books = [popular_book.book for popular_book in models.PopularBooks.objects.all()]
    return render(request, 'books/index.html', context={
        'books': books,
        'user': {
            'firstname': "Mahfuzur Rahman"
        }
        # 'user': None,
    })


def book_detail(request, id: int):
    book = models.Book.objects.get(id=id)
    similar_book_ids = recommend_book(book.id)
    similar_books = models.Book.objects.filter(id__in=similar_book_ids)

    return render(request, 'books/book_detail.html', context={
        'book': book,
        'recommendation': similar_books,
        'user': {
            'firstname': 'Mahfuzur Rahman'
        }
    })


def recommend_book(book_id: int):
    index = np.where(pivot_table == book_id)[0][0]
    similar_items = sorted(list(
        enumerate(similarity_scores[index])), key=lambda item: item[1], reverse=True)[1:6]

    return [item[0] for item in similar_items]
