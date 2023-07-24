from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=256, db_index=True)
    authors = models.ManyToManyField("Author", through="BookAuthor")
    isbn = models.CharField(max_length=13, db_index=True,
                            null=True, default=None)
    yearpublished = models.CharField(max_length=4, null=True, default=None)
    genres = models.ManyToManyField("Genre", through="BookGenre")
    thumbnailurl = models.CharField(max_length=1024, default="N/A")
    summary = models.CharField(max_length=6144, default="N/A")
    price = models.FloatField()
    quantity = models.IntegerField()

    createddate = models.DateField(auto_now_add=True)
    updateddate = models.DateField(auto_now=True)


class Author(models.Model):
    firstname = models.CharField(max_length=128)
    surname = models.CharField(max_length=256)
    email = models.EmailField(max_length=128)
    books = models.ManyToManyField(Book, through="BookAuthor")

    createddate = models.DateField(auto_now_add=True)
    updateddate = models.DateField(auto_now=True)

    @property
    def fullname(self):
        return f"{self.firstname} {self.surname}"


class Customer(models.Model):
    firstname = models.CharField(max_length=128)
    surname = models.CharField(max_length=256)
    email = models.EmailField(max_length=128)
    phonenumber = models.CharField(max_length=14)
    user = models.OneToOneField(User, db_index=True, on_delete=models.CASCADE)

    createddate = models.DateField(auto_now_add=True)
    updateddate = models.DateField(auto_now=True)

    @property
    def fullname(self):
        return f"{self.firstname} {self.surname}"


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, db_index=True, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, db_index=True, on_delete=models.CASCADE)

    createddate = models.DateField(auto_now_add=True)
    updateddate = models.DateField(auto_now=True)


class Genre(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    books = models.ManyToManyField(Book, through="BookGenre")


class BookGenre(models.Model):
    book = models.ForeignKey(Book, db_index=True, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, db_index=True, on_delete=models.CASCADE)


class Rating(models.Model):
    rating = models.IntegerField()
    book = models.ForeignKey(Book, db_index=True, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        Customer, db_index=True, on_delete=models.CASCADE)


class PopularBooks(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount = models.FloatField(default=0)
    review_submitted = models.BooleanField(default=False)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)


class Order(models.Model):
    class OrderStatus(models.IntegerChoices):
        NOT_PLACED = 0
        ORDER_PLACED = 1
        DELIVERED = 2

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    discount = models.FloatField(default=0)
    orderstatus = models.IntegerField(
        choices=OrderStatus.choices, default=OrderStatus.NOT_PLACED)

    # to be deleted
    orderplaced = models.BooleanField(default=False)
    orderdelivered = models.BooleanField(default=False)

    createddate = models.DateField(auto_now_add=True)
    updateddate = models.DateField(auto_now=True)
