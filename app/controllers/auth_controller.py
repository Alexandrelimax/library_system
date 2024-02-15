from flask import Blueprint, request, jsonify
from app import bcrypt
from database import Database
from app.repositories import UserRepository
from helpers.JWTFunctions import generate_token

auth_controller = Blueprint('auth', __name__)

@auth_controller.route('/', methods=['POST'])
def login():
    data = request.json
    connection = Database.init_connection()
    user_repository = UserRepository(connection)
    user_database = user_repository.get_user_by_email(data['email'])

    id_user, user, _, email_db, password_db, _ = user_database

    if email_db != data['email']:
        return jsonify('login invalido'), 401

    if not bcrypt.check_password_hash(password_db, data['password']):
        return jsonify('senha invalida'), 401

    token = generate_token(id_user, user)
    return jsonify({'message': 'bem vindo', 'token': token})


@auth_controller.route('/register', methods=['POST'])
def register():
    data = request.json
    connection = Database.init_connection()
    user_repository = UserRepository(connection)
    user_database = user_repository.get_user_by_email(data['email'])

    if user_database:
        return jsonify('este email já existe'), 401

    if data['password'] != data['confirm_password']:
        return jsonify('A senha e a confirmação de senha devem ser iguais'), 401

    hash_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user_db = user_repository.insert_user(data['first_name'], data['last_name'], data['email'], hash_password)

    token = generate_token(user_db[0], user_db[1])

    return jsonify({'message': 'usuario salvo', 'token': token}), 201
