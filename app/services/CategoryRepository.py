class CategoryRepository:
    def __init__(self, connection):
        self.connection = connection

    def get_category(self, category):
        self.connection.commit()
        cursor = self.connection.cursor()
        query = f'SELECT id FROM categories WHERE name = {category}'
        values = (category,)
        cursor.execute(query)

        id_category = cursor.fetchone()[0]
        print(id_category)
        return id_category
