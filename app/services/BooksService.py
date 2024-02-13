from collections import OrderedDict


class BooksServices:
    def __init__(self, connection):
        self.connection = connection

    def get_all_books(self):
        cursor = self.connection.cursor()

        query = 'SELECT * FROM BOOKS'

        cursor.execute(query)
        keys = [column[0] for column in cursor.description]
        books = list()
        for book in cursor.fetchall():
            id, name, description, url_img, status, author, created_at = book

            books.append({'id': id, 'name': name, 'description': description,
                          'url_img': url_img, 'status': status, 'author': author,
                          'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')})

        # books = [
        #     {'id': book[0], 'name': book[1], "description": book[2], "url_img": book[3], "status": book[4],"author": book[5], 'created_at': book[6].strftime('%Y-%m-%d %H:%M:%S') }
        #     for book in cursor.fetchall()]

        return books

    def get_books_by_category(self, category):
        cursor = self.connection.cursor()

        query = """
                SELECT b.id, b.name, b.description, b.url_img, b.status, b.author, c.name as categoria
                FROM books b
                inner join books_categories 
                on b.id = books_categories.id_books
                inner join categories c
                on c.id = books_categories.id_categories
                where c.name = %s

        """
        values = (category,)
        cursor.execute(query, values)
        books = list()
        for book in cursor.fetchall():
            id, name, description, url_img, status, author, category_name = book

            books.append({'id': id, 'name': name, 'description': description,
                          'url_img': url_img, 'status': status, 'author': author, 'category': category_name})

        return books

    def get_books_by_author(self, author):
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM books where author = %s', (author,))
        return [{'id': book[0], 'name': book[1], 'description': book[2],
                 'url_img': book[3], 'status': book[4], 'author': book[5]}
                for book in cursor.fetchall()]

    def get_book_by_id(self, id):
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM books where id = %s', (id,))
        print(cursor.description)
        keys = [column[0] for column in cursor.description]
        # print(keys)

        values = cursor.fetchone()
        book_date = list(values)
        book_date[6] = book_date[6].strftime('%Y-%m-%d %H:%M:%S')

        return dict(zip(keys, book_date))

    def rent_book(self):
        pass
