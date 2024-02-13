class BooksRepository:
    def __init__(self, connection) -> None:
        self.connection = connection

    def insert_book(self, name, description, url_image, author):
        cursor = self.connection.cursor()

        query = 'INSERT INTO books (name, description, url_img, status, author) VALUES (%s, %s, %s,%s, %s)'
        values = (name, description, url_image, 'available', author)
        # try:
        cursor.execute(query, values)
        return cursor.lastrowid

        # except:
        #     print(f'impossivel persistir')

    def associate_book_by_category(self, id_book, id_category):
        self.connection.commit()
        cursor = self.connection.cursor()
        query = f'insert into books_categories(id_categories, id_books) values({id_category}, {id_book})'
        values = (id_category, id_book)
        cursor.execute(query)
        self.connection.commit()
        print('salvo')
        cursor.close()

    def update_book(self, id, column, value):
        cursor = self.connection.cursor()

        query = 'UPDATE books SET %s = %s WHERE id = %s'
        values = (column, value, id)

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except:
            print(f'impossivel persistir')

    def delete_book(self, id):
        cursor = self.connection.cursor()

        query = 'delete from books WHERE  id = %s'
        values = (id)

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except:
            print(f'impossivel persistir')
