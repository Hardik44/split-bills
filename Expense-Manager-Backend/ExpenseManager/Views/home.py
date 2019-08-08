from datetime import datetime
from jwt import encode
from flask import request
from flask.json import jsonify
from ExpenseManager import app, config
from ExpenseManager.forms import RegisterForm, LoginForm
from ExpenseManager.repository import create_user
from ExpenseManager.models import User

url_prfix = '/api/v1'

@app.route('/')
def index():
    '''Home page for api'''
    return jsonify(message='welcome to expense manager. you are using v1 api.')

@app.route(url_prfix + '/login', methods = ['POST'])
def login():
    '''
    login method to log user in using email and password.
    it checks if email and pasword are correct or not
    and based on that it returns JWT token.
    '''
    if request.is_json:
        login_form = LoginForm.from_json(request.get_json())
        if login_form.validate() is True:
            user = User.query.filter_by(email=login_form.data['email']).first()
            if user and user.verify_password(login_form.data['password']):
                auth_token = _generate_token(user)
                return jsonify(token=auth_token), 200
            else:
                return jsonify(message="either email or password is wrong"), 400
        else:
            return jsonify(message="invalid data sent"), 400


@app.route(url_prfix + '/register', methods = ['POST'])
def register():
    '''
    Creates new user in database. first it will verify input
    with wtforms and if the inputs are valid then it will check
    if user already exists with given email or not. if user does
    not exists with given email then it will creat new user
    '''
    if request.is_json:
        register_form = RegisterForm.from_json(request.get_json())
        if register_form.validate() is True:
            user = User.query.filter_by(email=register_form.data['email']).first()
            if user:
                return jsonify(message="User with given email already exists"), 409
            else:
                try:
                    res = create_user(register_form)
                    return jsonify(message="Successfully added new user", user=res.data), 202
                except Exception as e:
                    print(e)
                    return jsonify(message="Unable add user now"), 500
        else:
            return jsonify({"message":"User data validation failed"}), 422
    else:
        return jsonify(message="The data sent to server was not in json format")


def _generate_token(user):
    '''
    Generates new JWT token for given user information.
    this token will be different for each time user logs in
    '''

    if user.role.name == 'admin':
        is_admin = True
    else:
        is_admin = False

    if user is not None:
        payload = {
            'id': user.id,
            'password_hash': user.password_hash,
            'date_issued': datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            'is_admin': is_admin,
            'username': user.username.title()
        }
        data = encode(payload, config['token_key'])
        return data
    else:
        return 'no token since user does no exists!'
