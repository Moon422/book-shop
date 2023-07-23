import random
import numpy as np
import pandas as pd
from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpRequest
from django.contrib.auth import login, authenticate, logout
from django.db import transaction
from . import models


pivot_table = pd.read_pickle("pivot_table.pkl")
similarity_scores = pd.read_pickle("similarity_score.pkl")


def book_cart_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    cart = models.Order.objects.get(customer_id=customer.id, orderplaced=False)

    if not cart:
        return render(request, "books/cart_view.html", {
            "user": customer,
            "cart": None
        })

    cart_items = models.OrderItem.objects.filter(order_id=cart.id)
    print(cart_items)

    cart_items = [
        {
            "id": item.id,
            "book": item.book,
            "quantity": item.quantity,
            "item_total": item.quantity * item.book.price
        }
        for item in cart_items
    ]

    return render(request, "books/cart_view.html", {
        "user": customer,
        "cart_items": cart_items
    })


def book_add_to_cart(request: HttpRequest):
    book_id = int(request.POST.get("book-id"))
    book_quantity = int(request.POST.get("book-quantity"))

    customer = models.Customer.objects.get(user_id=request.user.id)
    book = models.Book.objects.get(id=book_id)
    order = models.Order.objects.get(
        customer_id=customer.id, orderplaced=False)
    with transaction.atomic():
        if not order:
            order = models.Order.objects.create(
                customer=customer
            )
        order_item = models.OrderItem.objects.create(
            book=book,
            quantity=book_quantity,
            order=order
        )
    print(request.get_full_path())

    return HttpResponse()


def book_order_item_remove(request):
    pass


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return redirect("book_index")
        else:
            redirect("book_user_login")
    return render(request, "books/login.html")


def user_logout(request):
    logout(request)
    return redirect("book_index")


def index(request):
    books = get_popular_books()
    customer = None
    if request.user.id:
        customer = models.Customer.objects.get(user_id=request.user.id)
        print(customer)
    return render(request, 'books/index.html', context={
        'best_sellers': books,
        'user': customer
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
