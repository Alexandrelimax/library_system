
class UserRepository:
    def __init__(self, connection) -> None:
        self.connection = connection


    def insert_user(self, first_name, last_name, email, password):
        cursor = self.connection.cursor()

        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)'
        values = (first_name, last_name, email, password)
        # try:
        cursor.execute(query, values)
        self.connection.commit()
        print('salvo')
        cursor.close()
        # except:
        #     print(f'impossivel persistir')


    def update_user(self, id, column ,value):
        cursor = self.connection.cursor()

        query = 'UPDATE books SET %s = %s WHERE id = %s'
        values = (column, value, id)

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except:
            print(f'impossivel persistir')

    def delete_user(self, id):
        cursor = self.connection.cursor()

        query = 'delete from books WHERE  id = %s'
        values = (id)

        try:
            cursor.execute(query, values)
            self.connection.commit()
        except:
            print(f'impossivel persistir')

    def get_user_by_email(self, email):
        cursor = self.connection.cursor()
        print(email)
        query = 'SELECT * from users WHERE email = %s'
        values = (email,)
        print('estamos aqui')
        try:
            cursor.execute(query, values)
            user = cursor.fetchone()

            return user


        except:
            print(f'PROBLEMA É AQUI')

