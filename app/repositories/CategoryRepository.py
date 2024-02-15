class CategoryRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_category(self, category):
        self.connection.commit()
        cursor = self.connection.cursor()
        cursor.execute(f'SELECT id FROM categories WHERE name = "{category}"')

        id_category = cursor.fetchone()[0]
        return id_category
