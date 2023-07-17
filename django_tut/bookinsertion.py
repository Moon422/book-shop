from books import models

with open('Books.csv', 'r') as books_file:
    books = books_file.readlines()[1:]
    for idx, book in enumerate(books):
        authorname = book.split(',')[2]
        # types = set()

        # types.add(type(authorname))

        # try:
        #     names = authorname.split()
        #     print(idx, names)
        # except:
        #     print(authorname)

        # firstname = ' '.join(names[:-1])
        # surname = names[-1]
        # print((firstname, surname))
