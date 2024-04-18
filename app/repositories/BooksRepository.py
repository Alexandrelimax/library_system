class BooksRepository:
    def __init__(self, connection) -> None:
        self.connection = connection

    def insert_book(self, name, description, url_image, author):
        cursor = self.connection.cursor()
        
        query = 'INSERT INTO books (name, description, url_img, status, author) VALUES (%s, %s, %s,%s, %s)'
        values = (name, description, url_image, 'available', author)
        try:
            cursor.execute(query, values)
            return cursor.lastrowid
        except:
            print(f'impossivel persistir')

    def associate_book_by_category(self, id_book, id_category):
        self.connection.commit()
        cursor = self.connection.cursor()
        query = f'INSERT INTO books_categories(id_category, id_book) VALUES ({id_category}, {id_book})'
        try:
            cursor.execute(query)
            self.connection.commit()
        except:
            print(f'impossivel persistir')

    def update_book(self, id, column, value):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f'UPDATE books SET {column} = {value} WHERE id = {id}')
            self.connection.commit()
        except:
            print(f'impossivel persistir')

    def delete_book(self, id):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f'DELETE FROM books WHERE  id = {id}')
            self.connection.commit()
        except:
            print(f'impossivel persistir')
