from django.contrib import admin
from . import models

# Register your models here.


class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "quantity")


class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname", "email")


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("id", "fullname", "email", "phonenumber")


admin.site.register(models.Book, BookAdmin)
admin.site.register(models.Author, AuthorAdmin)
admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.BookAuthor)
admin.site.register(models.Genre)
admin.site.register(models.BookGenre)
admin.site.register(models.OrderItem)
admin.site.register(models.Order)
admin.site.register(models.Rating)
