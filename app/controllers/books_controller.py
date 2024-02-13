import json

from flask import Blueprint, jsonify, request, Response, make_response
from app.services import BooksRepository
from app.services import BooksServices
from app.services import CategoryRepository
from database import Database

books_controller = Blueprint('books', __name__)


@books_controller.route('/books/', methods=['GET'])
def get_all_books():
    conn = Database.init_connection()
    print('aqui')
    books_service = BooksServices(conn)
    books = books_service.get_all_books()
    return jsonify(books)
    # return Response(json.dumps(books), content_type='application/json charset=utf-8')

@books_controller.route('/', methods=['POST'])
def insert_new_book():
    data = request.json
    connection = Database.init_connection()
    book_repo = BooksRepository(connection)
    category_repo = CategoryRepository(connection)

    id_book = book_repo.insert_book(data['name'], data['description'], data['url_img'], data['author'])

    id_category = category_repo.get_category(data['category'])

    book_repo.associate_book_by_category(id_book, id_category)

    return jsonify({'salvo': 'ok'}), 201


@books_controller.route('/books/category/', methods=['GET'])
def get_book_by_category():
    category = request.args.get('category')
    connection = Database.init_connection()
    books_service = BooksServices(connection)
    books_by_category = books_service.get_books_by_category(category)
    # return jsonify(book)
    return Response(json.dumps(books_by_category), content_type='application/json; charset=utf-8')


@books_controller.route('/books/author/', methods=['GET'])
def get_book_by_author():
    author = request.args.get('author')
    connection = Database.init_connection()
    books_service = BooksServices(connection)
    books_by_author = books_service.get_books_by_author(author)
    # return jsonify(book)
    return Response(json.dumps(books_by_author), content_type='application/json; charset=utf-8')


@books_controller.route('/books/<int:id_book>', methods=['GET'])
def get_book(id_book):
    connection = Database.init_connection()
    books_service = BooksServices(connection)
    book = books_service.get_book_by_id(id_book)
    # return jsonify(book)
    return Response(json.dumps(book), content_type='application/json; charset=utf-8')



# @books_controller.route('/rent/<int:id_book>', methods=['POST'])
# def rent_a_book(id_book):
#





