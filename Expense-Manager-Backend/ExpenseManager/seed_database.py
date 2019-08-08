from random import randint
from datetime import datetime
from calendar import monthrange
from ExpenseManager import config
from ExpenseManager.models import db, Category, Expense, CategoriesToUsers, Role, User
from json import load

def seed_postgres():
    '''
    This function provieds initial seed data for application
    '''

    if Role.query.all() == []:
        roles = [Role('admin'), Role('user')]
        for role in roles:
            db.session.add(role)
        db.session.commit()

    if User.query.all() == []:
        #adding admin user
        try:
            name = config['admin_name']
            email = config['admin_email']
            pwd = config['admin_password']
            admin_role_id = Role.query.filter_by(name='admin').first().id
            admin = User(name, email, pwd, admin_role_id)
            db.session.add(admin)
            db.session.commit()
        except Exception as e:
            print(e)
            print("no config file found or fields are misssing from config file")

        #defining normal user

        with open('test_users.json') as users:
            _users = load(users)
        users = []
        user_role_id = Role.query.filter_by(name='user').first().id
        for user in _users:
            users.append(User(user['name'], user['email'], user['password'], user_role_id))

    if Category.query.all() == []:
        categories = [
            Category('entertainment', True),
            Category('food', True),
            Category('education', True)
        ]
        for cat in categories:
            db.session.add(cat)
        db.session.commit()

        #assiging default categories to the users and adding user into database
        for user in users:
            for cat in categories:
                ctou = CategoriesToUsers() #creating association object
                ctou.category = cat #assign category to association object
                user.categories_to_users.append(ctou) #append association object to user
            db.session.add(user)
        db.session.commit()

    if Expense.query.all() == []:
        categories_to_users_ids = CategoriesToUsers.query.with_entities(CategoriesToUsers.id).all()
        categories_to_users_ids = [cat[0] for cat in categories_to_users_ids]
        max_ctou = max(categories_to_users_ids)
        min_ctou = min(categories_to_users_ids)
        for _ in range(500):
             year = randint(2015, 2016)
             month = randint(1, 12)
             day = randint(1, monthrange(year, month)[1])
             hour = randint(0, 23)
             minute = randint(0, 59)
             second = randint(0, 59)
             date_added = datetime(year, month, day, hour, minute, second)
             expense = Expense(randint(min_ctou, max_ctou), randint(10, 1000), date_added)
             db.session.add(expense)
        db.session.commit()
