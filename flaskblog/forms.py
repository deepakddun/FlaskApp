from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField , TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, Required, ValidationError
from flaskapp.flaskblog.models import User
from flask_login import current_user


# def duplicate_validator(form, field):
#     # user = User.query.filter_by(username=field.data).first()
#     user = User.query.filter(or_(User.username==field.data, User.email==field.data))
#     print(field.name)
#     field_name = field.name
#     if user:
#         raise ValidationError(f" {field_name} already exists. Please use a different one ")


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired("This is required"), Length(min=2, max=20)])
    email = StringField('Email', validators=[Required(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Sign up')

    def validate_username(form, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError(f" Username already exists. Please use a different one. ")

    def validate_email(form, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError(f" Email already exists. Please use a different one. ")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired("This is required"), Length(min=2, max=20)])
    email = StringField('Email', validators=[Required(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(form, field):
        print("Testing")
        if current_user.username != field.data:
            user = User.query.filter_by(username=field.data).first()
            if user:
                print("Testing 2")
                raise ValidationError(f" Username already exists. Please use a different one. ")

    def validate_email(form, field):
        if current_user.email != field.data:
            user = User.query.filter_by(email=field.data).first()
            if user:
                raise ValidationError(f" Email already exists. Please use a different one. ")


class PostForm(FlaskForm):

    title = StringField("Title",validators=[DataRequired()])
    content = TextAreaField("Post",validators=[DataRequired()])
    submit = SubmitField("Post")
