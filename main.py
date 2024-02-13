from app import app
from app.controllers import books_controller
from app.controllers import auth_controller
from database import Database

conn = Database.init_connection()
app.register_blueprint(auth_controller, urlprefix='/')
app.register_blueprint(books_controller, url_prefix='/home')


if __name__ == '__main__':
    app.run(debug=True)