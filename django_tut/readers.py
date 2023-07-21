import faker
import random
from books import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

count = models.Book.objects.count()

readers = []

for i in range(1000):
    fake = faker.Faker()
    firstname = fake.first_name()
    surname = fake.last_name()
    suffix = count + i
    separator = random.choice(['', '.', '_'])
    email = firstname.lower() + separator + surname.lower() + \
        str(suffix) + fake.free_email_domain()

    readers.append(
        models.Customer(
            firstname=firstname,
            surname=surname,
            email=email,
            phonenumber=f"{random.choice(['+88017', '+88019', '+88018'])}{fake.numerify('#' * 8)}",
            user=User.objects.create(
                username=f'{surname}{suffix}',
                password=make_password("Zxcv!@34")
            )
        )
    )

models.Customer.objects.bulk_create(readers)
