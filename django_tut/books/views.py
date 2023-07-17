from django.shortcuts import render
from . import models


# Create your views here.
def index(request):
    books = list(models.Book.objects.all())
    return render(request, 'books/index.html', context={
        'books': books,
        'user': {
            'firstname': "Mahfuzur Rahman"
        }
        # 'user': None,
    })


def book_detail(request, id: int):
    book = models.Book.objects.get(id=id)

    return render(request, 'books/book_detail.html', context={
        'book': book,
        'user': {
            'firstname': 'Mahfuzur Rahman'
        }
    })
