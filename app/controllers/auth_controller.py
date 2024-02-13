from flask import Blueprint, request, jsonify

from app.services import UserRepository
from database import Database
auth_controller = Blueprint('auth', __name__)

@auth_controller.route('/', methods=['POST'])
def login():
    data = request.json
    connection = Database.init_connection()
    user_repository = UserRepository(connection)
    user_database = user_repository.get_user_by_email(data['email'])

    email_db = user_database[3]
    password_db = user_database[4]

    if email_db != data['email']:
        return jsonify('login invalido'), 401

    if password_db != data['password']:
        return jsonify('senha invalida'), 401

    else:
        return jsonify({'message': 'bem vindo'})

@auth_controller.route('/register', methods=['POST'])
def register():
    data = request.json
    connection = Database.init_connection()
    user_repository = UserRepository(connection)
    user = user_repository.get_user_by_email(data['email'])

    if user:
        return jsonify('este email já existe'), 401

    if data['password'] != data['confirm_password']:
        return jsonify('A senha e a confirmação de senha devem ser iguais'), 401

    else:
        user_repository.insert_user(data['first_name'], data['last_name'], data['email'], data['password'])
        return jsonify({'message': 'usuario salvo'})
