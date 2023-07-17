from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Book)
admin.site.register(models.Author)
admin.site.register(models.Customer)
admin.site.register(models.BookAuthor)
admin.site.register(models.Genre)
admin.site.register(models.BookGenre)
admin.site.register(models.OrderItem)
admin.site.register(models.Order)
