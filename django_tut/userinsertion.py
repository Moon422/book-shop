from books import models

data = [{'firstname': f'Firstname{i+1}', 'surname': f'Surname{i+1}',
         'email': f'email{i+1}@email.com', 'phonenumber': '+8801712345678'} for i in range(278860)]

models.Customer.objects.bulk_create([models.Customer(
    firstname=d['firstname'], surname=d['surname'], email=d['email'], phonenumber=d['phonenumber']) for d in data])
