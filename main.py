from app import app
from database import Database
from app.controllers import books_controller
from app.controllers import auth_controller


conn = Database.init_connection()
app.config['secret'] = 'senha muito secreta.'


app.register_blueprint(auth_controller, urlprefix='/')
app.register_blueprint(books_controller, url_prefix='/books')

if __name__ == '__main__':
    app.run(debug=True)
