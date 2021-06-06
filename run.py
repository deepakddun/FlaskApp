# from flask import Flask, render_template, url_for, redirect, flash, get_flashed_messages
# from forms import RegistrationForm, LoginForm
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime
#
# app = Flask(__name__)
# app.config['SECRET_KEY'] = "b94a3ba00537c35b574a91a04d12deb2"
# username = 'deepak'
# password = 'Sterlite152@'g
# server = 'localhost'
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{username}:{password}@{server}/flaskdb"
# db = SQLAlchemy(app)

from flaskapp.flaskblog import app


if __name__ == '__main__':
    app.run(debug=True)
