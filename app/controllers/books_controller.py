import json
import os.path

import jwt
from app import app
from flask import Blueprint, jsonify, request, Response
from app.repositories import BooksRepository
from app.services import BooksServices
from app.repositories import CategoryRepository
from database import Database

books_controller = Blueprint('books', __name__)
from werkzeug.utils import secure_filename
import os
from app import app
UPLOAD_FOLDER = 'C:/Users/alexandre.lima_ipnet/PycharmProjects/library1/upload/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import csv
from flask import send_file, send_from_directory
# UPLOAD_FOLDER = os.path.join(os.getcwd(), 'upload')



@books_controller.route('/', methods=['GET'])
def get_all_books():
    conn = Database.init_connection()
    books_service = BooksServices(conn)
    books = books_service.get_all_books()
    print(books)
    # return jsonify(books)
    return Response(json.dumps(books), content_type='application/json charset=utf-8')


@books_controller.route('/add_book', methods=['POST'])
def insert_new_book():
    data = request.json
    connection = Database.init_connection()
    book_repo = BooksRepository(connection)
    category_repo = CategoryRepository(connection)

    id_book = book_repo.insert_book(data['name'], data['description'], data['url_img'], data['author'])

    for category in data['categories']:
        id_category = category_repo.get_category(category)
        book_repo.associate_book_by_category(id_book, id_category)

    return jsonify({'salvo': 'ok'}), 201


@books_controller.route('/category', methods=['GET'])
def get_book_by_category():
    category = request.args.get('category')
    connection = Database.init_connection()
    books_service = BooksServices(connection)

    books_by_category = books_service.get_books_by_category(category)

    if not books_by_category:
        return jsonify({'alert': 'Não há esta categoria no sistema'})

    return Response(json.dumps(books_by_category), content_type='application/json; charset=utf-8')


@books_controller.route('/author', methods=['GET'])
def get_book_by_author():
    author = request.args.get('author')
    connection = Database.init_connection()
    books_service = BooksServices(connection)

    books_by_author = books_service.get_books_by_author(author)
    if not books_by_author:
        return jsonify({'alert': 'Não há este autor no sistema'})

    return Response(json.dumps(books_by_author), content_type='application/json; charset=utf-8')


@books_controller.route('/<int:id_book>', methods=['GET'])
def get_book(id_book):
    connection = Database.init_connection()
    books_service = BooksServices(connection)

    book = books_service.get_book_by_id(id_book)
    return Response(json.dumps(book), content_type='application/json; charset=utf-8')


@books_controller.route('/rent/<int:id_book>', methods=['POST'])
def rent_a_book(id_book):
    connection = Database.init_connection()
    books_service = BooksServices(connection)
    token = request.headers.get('Authorization')

    if not token:
        return jsonify(message='Somente usuários cadastrados podem alugar livros')

    try:
        user_payload = jwt.decode(token, app.config['secret'], algorithms=['HS256'])
        books_service.rent_book(user_payload['id'], id_book)
        return jsonify({'message': 'Voce alugou o livro, parabéns!'})

    except jwt.ExpiredSignatureError:
        return jsonify({'Acesso negado': 'Token expirado'})
    except jwt.InvalidTokenError:
        return jsonify({'Acesso negado': 'Token inválido'})


@books_controller.route('/returnbook/<int:id_book>', methods=['PUT'])
def return_book(id_book):
    connection = Database.init_connection()
    books_service = BooksServices(connection)
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'Acesso negado': 'Somente usuários cadastrados podem alugar livros'})

    try:
        user_payload = jwt.decode(token, app.config['secret'], algorithms=['HS256'])
        books_service.return_book(user_payload['id'], id_book)
        return jsonify({'message': 'O livro foi devolvido'})

    except jwt.ExpiredSignatureError:
        return jsonify({'Acesso negado': 'Token expirado'})
    except jwt.InvalidTokenError:
        return jsonify({'Acesso negado': 'Token inválido'})


@books_controller.route('/csv/', methods=['POST'])
def upload_file_by_csv():
    connection = Database.init_connection()
    book_repo = BooksRepository(connection)
    category_repo = CategoryRepository(connection)

    file = request.files['files']
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    save_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
    file.save(save_path)

    with open(save_path, 'r') as new_file:
        data = new_file.read()
        lines = data.split('\n')
        content_list = [row.split(',') for row in lines]

        for index, row in enumerate(content_list):
            if index != 0:
                print(row)
                name, description, url_img, author, category = row
                print(name, description, url_img, author, category)

                id_book = book_repo.insert_book(name, description, url_img, author)

                id_category = category_repo.get_category(category)
                book_repo.associate_book_by_category(id_book, id_category)


    return jsonify({'message': 'recebido'})


@books_controller.route('/download/', methods=['GET'])
def send_file_by_csv():
    conn = Database.init_connection()
    books_service = BooksServices(conn)
    books = books_service.get_all_books()

    with open(f'{UPLOAD_FOLDER}/downloadfile.csv', 'w') as file:
        writer = csv.writer(file)
        header = books[0].keys()
        writer.writerow(tuple(header))
        for book in books:
            writer.writerow((book['id'], book['name'], book['description'], book['url_img'], book['status'], book['author'], book['created_at']))

    return send_file(f'{app.config['UPLOAD_FOLDER']}/downloadfile.csv', as_attachment=True)




