from functools import wraps
from jwt import decode, DecodeError
from flask import request, jsonify, g
from ExpenseManager import config
from ExpenseManager.models import User

token_key = config['token_key']

def auth_user(role):
    '''
    This function decorates flask route function. it will authenticate
    user from authorization token and checks if user is allowed to access
    requested resourse by checking their roles
    '''
    def auth_user_wrapper(f):
        '''
        auth_user wrapper function
        '''
        @wraps(f)
        def view(*args, **kwargs):
            '''
            auth_user wrapper defination
            '''
            user_token = request.headers.get('Authorization')
            if user_token is not None:
                try:
                    user_data = decode(user_token, key=token_key)
                    user = User.query.filter_by(id=user_data['id'], password_hash=user_data['password_hash']).first()
                    if user is not None:
                        if user.role.name == role:
                            g.user = user
                            return f(*args, **kwargs)
                        else:
                            return jsonify(message='you are not allowed to acces this resource(s)')
                    else:
                        raise DecodeError
                except DecodeError as d:
                    return jsonify(message='Invalid Token')
            else:
                return jsonify(message='authorization header is missing from request')
        return view
    return auth_user_wrapper
