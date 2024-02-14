class BooksServices:
    def __init__(self, connection):
        self.connection = connection

    def get_all_books(self):
        cursor = self.connection.cursor()
        query = 'SELECT * FROM BOOKS'
        cursor.execute(query)
        # books = list()
        # for book in cursor.fetchall():
        #     id, name, description, url_img, status, author, created_at = book
        #
        #     books.append({'id': id, 'name': name, 'description': description,
        #                   'url_img': url_img, 'status': status, 'author': author,
        #                   'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S')})
        books = [
            {'id': book[0], 'name': book[1], "description": book[2], "url_img": book[3], "status": book[4],"author": book[5], 'created_at': book[6].strftime('%Y-%m-%d %H:%M:%S') }
            for book in cursor.fetchall()]

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
        keys = [column[0] for column in cursor.description]
        values = cursor.fetchone()
        book_date = list(values)
        book_date[6] = book_date[6].strftime('%Y-%m-%d %H:%M:%S')

        return dict(zip(keys, book_date))

    def rent_book(self, id_user, id_book):
        cursor = self.connection.cursor()
        query = f'INSERT INTO books_transactions (return_date, id_user, id_book) VALUES (null,{id_user},{id_book})'
        cursor.execute(query)
        self.connection.commit()

    def return_book(self, id_user, id_book):
        cursor = self.connection.cursor()
        query = f'SELECT * FROM books_transactions WHERE id_user = {id_user} AND id_book = {id_book}'
        cursor.execute(query)
        id_transaction = cursor.fetchone()[0]
        self.connection.commit()

        self.update_return_book(id_transaction)

    def update_return_book(self, id):
        cursor = self.connection.cursor()
        query = f'UPDATE books_transactions SET return_date = CURRENT_TIMESTAMP() WHERE ID  = {id}'
        cursor.execute(query)
        self.connection.commit()







