from wtforms import Form
from wtforms.fields import StringField, PasswordField, DateField, FloatField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Length, Email

class RegisterForm(Form):
    '''
    wtform for registration
    '''
    user_name = StringField(validators=[Length(3, 80)])
    email = EmailField(validators=[Email()])
    password = PasswordField()

class LoginForm(Form):
    '''
    wtform for login
    '''
    email = EmailField(validators=[Email()])
    password = PasswordField()

class GetExpenseDetailsForm(Form):
    '''
    wtform for getting expense details
    '''
    start_date = DateField()
    end_date = DateField()

class AddExpenseDetailsForm(Form):
    '''
    wtform for adding expense
    '''
    category = StringField(validators=[Length(3, 80)])
    amount = FloatField()
    description = StringField(validators=[Length(0, 100)])

class AddCategoryForm(Form):
    '''
    wtform for adding category
    '''
    name = StringField(validators=[Length(3, 30)])

class AddGroupForm(Form):
    group_name = StringField(validators=[Length(3, 30)])

class AddFriendToGroupForm(Form):
    group_name = StringField(validators=[Length(3, 30)])
    friend_name = StringField(validators=[Length(3, 30)])

class RemoveFriendFromGroupForm(Form):
    group_name = StringField(validators=[Length(3, 30)])
    friend_name = StringField(validators=[Length(3, 30)])
