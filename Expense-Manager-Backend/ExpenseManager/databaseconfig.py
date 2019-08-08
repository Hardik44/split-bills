from flask_sqlalchemy import SQLAlchemy
from ExpenseManager import app, config

def connect_postgres():
    '''
    function used to connect to postgres sql. configuration for
    postgres should be stored in config.json in the root directory
    of project
    '''
    try:
        postgres_url = config['postgres_url']
    except Exception as e:
        print("no 'postgres_url' field in config or no config file is present")
        raise e

    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = postgres_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        return db
    except Exception as e:
        print("postgres database connection error")
    