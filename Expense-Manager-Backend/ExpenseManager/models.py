from ExpenseManager.databaseconfig import connect_postgres
import json
from datetime import datetime
from ExpenseManager import app
from werkzeug.security import generate_password_hash, check_password_hash

db = connect_postgres()
# uncomment following lines to create fresh database with fresh data 
# for every time you run the app
# WARNING: ALL THE OLD DATA WILL BE DELETED AND NEW DATA WILL BE ADDED FROM
# seed_database.py FILE

# db.engine.execute("drop schema if exists public cascade")
# db.engine.execute("create schema public")

class Role(db.Model):
    '''
    SQLAlchemy Role model for roles table
    '''

    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role: %r>' % self.name


class User(db.Model):
    '''
    SQLAlchemy User model for users table
    '''

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    date_of_registration = db.Column(db.DateTime, nullable=False, default = datetime.utcnow)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', uselist = False, lazy='joined')
    categories_to_users = db.relationship('CategoriesToUsers')

    def __init__(self, username, email, password, role_id):
        self.username = username
        self.email = email
        self.password = password
        self.role_id = role_id

    def __repr__(self):
        return '<User: %r>' % self.username

    @property
    def password(self):
        raise AttributeError('password: write only field')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.email

class Category(db.Model):
    '''
    SQLAlchemy Category model for categories table
    '''

    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False, unique=True)
    is_default = db.Column(db.Boolean, default = False, nullable = False)

    def __init__(self, name, is_default = False):
        self.name = name
        self.is_default = is_default

    def __repr__(self):
        return '<Category: %r>' % self.name

class Expense(db.Model):
    '''
    SQLAlchemy Expense model for expenses table
    '''

    __tablename__ = 'expenses'
    category_to_user_id =  db.Column(db.Integer, db.ForeignKey('categories_to_users.id'), nullable = False, primary_key = True)
    date_added = db.Column(db.DateTime, default = datetime.utcnow, nullable = False, primary_key = True)
    amount = db.Column(db.Float, nullable = False)
    description = db.Column(db.String(100))

    def __init__(self, ctou, amount, date_added, description=None):
        self.category_to_user_id = ctou
        self.amount = amount
        self.date_added = date_added
        self.description = description

    def __repr__(self):
        return '<Expense: %r>' % self.amount 

class CategoriesToUsers(db.Model):
    '''
    SQLAlchemy CategoriesToUsers model for categories_to_users table
    '''

    __tablename__ = 'categories_to_users'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category')

    def __repr__(self):
        return '<CategoriesToUsers: {} {} {}>'.format(self.id, self.user_id, self.category_id)

class ExpenseGroup(db.Model):
    __tablename__ = 'expense_group'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False, unique=True)
    # group_expense = db.Column(db.Float, nullable = False, default = 0)

class ExpenseGroupToUsers(db.Model):
    __tablename__ = 'expense_group_to_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    expense_group_id = db.Column(db.Integer, db.ForeignKey('expense_group.id'))
    # group_share = db.Column(db.Float, nullable = False, default = 0)


db.create_all()
