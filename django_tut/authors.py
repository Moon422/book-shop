import random
import faker
import pandas as pd
from books import models

ratings_df = pd.read_csv('../books_data/ratings.csv')
books_df = pd.read_csv('../books_data/books.csv')

authors_with_commas = books_df.authors.unique()

names = set()

for authors in authors_with_commas:
    authors_list = [author_name.strip() for author_name in authors.split(',')]
    for author in authors_list:
        names.add(author)

authors = []

for name in names:
    names = name.split()
    surname = names[-1]
    firstname = ' '.join(names[:-1])
    separator = random.choice(['', '.', '_'])
    fake = faker.Faker()
    email = names[0].lower()

    for name in names[1:]:
        separator = random.choice(['', '.', '_'])
        email += separator + name.lower()

    suffix = str(random.randint(0, 999))
    email += suffix + '@' + fake.free_email_domain()

    authors.append(models.Author(firstname=firstname,
                   surname=surname, email=email))

models.Author.objects.bulk_create(authors)
