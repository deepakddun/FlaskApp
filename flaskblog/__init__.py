from flask import Flask

from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = "b94a3ba00537c35b574a91a04d12deb2"
username = 'deepak'
password = 'Sterlite152@'
server = 'localhost'
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{username}:{password}@{server}/flaskdb"
db = SQLAlchemy(app)

from flaskapp.flaskblog import routes
