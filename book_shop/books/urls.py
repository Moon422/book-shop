from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="book_index"),
    path('<int:id>', views.book_detail, name="book_book_detail"),
    path('surprise', views.book_suprise, name="book_book_surprise"),
    path('add_to_cart', views.book_add_to_cart, name="book_book_add_to_cart"),
    path('order_item_remove', views.book_order_item_remove,
         name="book_book_order_item_remove"),
    path('place_order', views.place_order, name="book_place_order"),
    path('cancel_order', views.cancel_order, name="book_cancel_order"),
    path('order_item_review', views.order_item_review,
         name="book_order_item_review"),
    path('cart', views.book_cart_view, name="book_book_cart_view"),
    path('login', views.user_login, name="book_user_login"),
    path('signout', views.user_logout, name="book_user_logout")
]
