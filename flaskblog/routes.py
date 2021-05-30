from flask import render_template, url_for, redirect, flash, get_flashed_messages
from flaskapp.flaskblog.models import  User , Post
from flaskapp.flaskblog.forms import  RegistrationForm, LoginForm
from flaskapp.flaskblog import app


posts = [
    {
        "title": "Blog post 1",
        "user": "Deepak Sharma",
        "content": "This is my first blog",
        "date": "May 27, 2021"
    },
    {
        "title": "Blog post 2",
        "user": "Shree Kumar",
        "content": "This is my first blog",
        "date": "May 25, 2021"
    }
]


@app.route("/")
def home():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return "About"


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Account logged in  {form.email.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

