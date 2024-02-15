class UserRepository:
    def __init__(self, connection) -> None:
        self.connection = connection

    def insert_user(self, first_name, last_name, email, password):
        cursor = self.connection.cursor()

        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)'
        values = (first_name, last_name, email, password)
        try:
            cursor.execute(query, values)
            self.connection.commit()
            return self.get_user_by_email(email)
        except:
            print(f'impossivel persistir')

    def update_user(self, id, column, value):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f'UPDATE books SET {column} = {value} WHERE id = {id}')
            self.connection.commit()
        except:
            print(f'impossivel persistir')

    def delete_user(self, id):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f'delete from books WHERE  id = {id}')
            self.connection.commit()
        except:
            print(f'impossivel persistir')

    def get_user_by_email(self, email):
        cursor = self.connection.cursor()
        try:
            cursor.execute(f'SELECT * from users WHERE email = "{email}"')
            return cursor.fetchone()
        except:
            print(f'PROBLEMA É AQUI')
