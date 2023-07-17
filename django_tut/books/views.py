import pandas as pd
from django.shortcuts import render, HttpResponse
from . import models

popular_df = pd.read_pickle('books/popular.pkl')
pt = pd.read_pickle('books/pt.pkl')
books = pd.read_pickle('books/books.pkl')
similarity_scores = pd.read_pickle('books/similarity_scores.pkl')


# Create your views here.
def index(request):
    books_data = []

    for index in books.index:
        books_data.append({
            'id': index,
            'title': books['Book-Title'][index],
            'author': books['Book-Author'][index],
            'thumbnailurl': books['Image-URL-M'][index],
            'quantity': 15,
            'price': 15.99
        })

    return render(request, 'books/index.html', context={
        'books': books_data[:50],
        'user': {
            'firstname': "Mahfuzur Rahman"
        }
        # 'user': None,
    })


def book_detail(request, id: int):
    book = books.iloc[id]

    book = {
        'id': id,
        'title': book['Book-Title'],
        'summary': 'Random Summary',
        'author': book['Book-Author'],
        'thumbnailurl': book['Image-URL-M'],
        'quantity': 15,
        'price': 15.99
    }

    similar_items = sorted(
        list(enumerate(similarity_scores[id])), key=lambda x: x[1], reverse=True)[1:6]

    similar_items_ids = [id for (id, _) in similar_items]
    similar_books = books.iloc[similar_items_ids]
    print(similar_books)

    recommendation = [{
        'id': index,
        'title': books['Book-Title'][index],
        'thumbnailurl': books['Image-URL-M'][index],
        'quantity': 15,
        'price': 15.99
    } for index in similar_books.index]

    return render(request, 'books/book_detail.html', context={
        'book': book,
        'user': {
            'firstname': 'Mahfuzur Rahman'
        },
        'recommendation': recommendation
    })
