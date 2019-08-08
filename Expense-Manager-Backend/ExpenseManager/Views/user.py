from ExpenseManager import app
from flask import request, jsonify, g, request
from ExpenseManager.models import User
from ExpenseManager.auth_user import auth_user
from ExpenseManager.models import db, CategoriesToUsers, Expense, User, Category
from ExpenseManager.forms import GetExpenseDetailsForm, AddExpenseDetailsForm, AddCategoryForm, AddGroupForm, \
    AddFriendToGroupForm, RemoveFriendFromGroupForm
from ExpenseManager.repository import get_expense_details, get_categories, add_expense_details, add_category_details
from ExpenseManager.repository import create_new_group, add_friend_to_groups, remove_friend_from_groups, add_expense_to_group

pre = '/api/v1/user'

@app.route(pre + '/expense_details', methods=['POST'])
@auth_user('user')
def expense_details():
    '''
    Get expense details for a particular user from repository
    '''
    try:
        if request.is_json and request.data:
            get_expense_form = GetExpenseDetailsForm.from_json(request.get_json())
            if get_expense_form.validate() is True:
                expenses = get_expense_details(
                    g.user,
                    start_date=get_expense_form.data['start_date'],
                    end_date=get_expense_form.data['end_date']
                )
            else:
                return jsonify(message='invalid json data'), 400
        else:
            expenses = get_expense_details(g.user,)
        return jsonify(expenses), 200
    except Exception as e:
        print(e)
        return jsonify(message='unable to get the data'), 500

@app.route(pre + '/expense_details/<string:category_name>', methods=['POST'])
@auth_user('user')
def expense_details_category_wise(category_name):
    '''
    Get expense details for a particular user from repository
    and filter it by given category name
    '''
    try:
        categories = get_categories(g.user)
        categories = [cat.name for cat in categories]
        try: 
            category = categories[categories.index(category_name.lower())]
        except:
            category = None
        if category is None:
            return jsonify(message='this user does not have specified category'), 400
        else:
            expenses = get_expense_details(g.user, category)
            return jsonify(expenses), 200
    except Exception as e:
        print(e)
        return jsonify(message='unable to get the data'), 500

@app.route(pre + '/categories', methods=['GET'])
@auth_user('user')
def categories_details():
    '''
    Get category details for a particular user from repository
    '''
    try:
        categories = get_categories(g.user)
        return jsonify(categories=[cat.name.title() for cat in categories]), 200
    except Exception as e:
        print(e)
        return jsonify(message='unable to get the data'), 500


@app.route(pre + '/add_expense', methods=['POST'])
@auth_user('user')
def add_expense():
    '''
    Add expense details for a particular user from expense form
    submitted by user
    '''
    try:
        if request.is_json and request.data:
            add_expense_form = AddExpenseDetailsForm.from_json(request.get_json())
            if add_expense_form.validate():
                res = add_expense_details(g.user, add_expense_form)
                return jsonify(message='successfully added new resource', expense_resource=res), 201
            else:
                return jsonify(message='invalid json data'), 400
        else:
            return jsonify(message='request is not in json format or body is empty'), 400
    except Exception as e:
        print(e)
        return jsonify(message='unable to add new resource'), 500

@app.route(pre + '/add_category', methods=['POST'])
@auth_user('user')
def add_category():
    '''
    Add category details for a particular user from category form
    submitted by user
    '''
    try:
        if request.is_json and request.data:
            add_category_form = AddCategoryForm.from_json(request.get_json())
            if add_category_form.validate():
                res = add_category_details(g.user, add_category_form)
                return jsonify(message='successfully added new resource', category_resource=res), 201
            else:
                return jsonify(message='invalid json data'), 400
        else:
            return jsonify(message='request is not in json format or body is empty'), 400
    except Exception as e:
        print(e)
        return jsonify(message='unable to add new resource'), 500

@app.route(pre + '/create_group', methods=['POST'])
@auth_user('user')
def create_group():
    try:
        if request.is_json and request.data:
            add_group_form = AddGroupForm.from_json(request.get_json())
            if add_group_form.validate():
                res = create_new_group(g.user, add_group_form)
                return jsonify(message='successfully added new resource', group_resource=res), 201
        else:
            return jsonify(message='request is not in json format or body is empty'), 400
    except Exception as e:
        print(e)
        return jsonify(message='unable to add new resource'), 500

@app.route(pre + '/add_friend_to_group', methods=['POST'])
@auth_user('user')
def add_friend_to_group():
    try:
        if request.is_json and request.data:
            add_group_form = AddFriendToGroupForm.from_json(request.get_json())
            if add_group_form.validate():
                res = add_friend_to_groups(g.user, add_group_form)
                return jsonify(message='successfully added new resource', group_resource=res), 201
        else:
            return jsonify(message='request is not in json format or body is empty'), 400
    except Exception as e:
        print(e)
        return jsonify(message='unable to add new resource'), 500

@app.route(pre + '/remove_friend_from_group', methods=['POST'])
@auth_user('user')
def remove_friend_from_group():
    try:
        if request.is_json and request.data:
            remove_from = RemoveFriendFromGroupForm.from_json(request.get_json())
            if remove_from.validate():
                res = remove_friend_from_groups(g.user, remove_from)
                return jsonify(message='successfully deleted resource', group_resource=res), 201
        else:
            return jsonify(message='request is not in json format or body is empty'), 400
    except Exception as e:
        print(e)
        return jsonify(message='unable to delete resource'), 500

# @app.route(pre + '/add_group_expense', methods=['POST'])
# @auth_user('user')
# def add_group_expense():
#     try:
#         if request.is_json and request.data:
#             res = add_expense_to_group(g.user, request.get_json())
#             return jsonify(message='successfully added new resource', group_resource=res), 201
#         else:
#             return jsonify(message='request is not in json format or body is empty'), 400
#     except Exception as e:
#         print(e)
#         return jsonify(message='unable to add new resource'), 500
