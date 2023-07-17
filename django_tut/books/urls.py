from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="book_index"),
    path('<int:id>', views.book_detail, name="book_book_detail")
]
