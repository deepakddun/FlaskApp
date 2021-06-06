from flask import render_template, url_for, redirect, flash, get_flashed_messages, request ,abort
from flaskapp.flaskblog.models import User, Post
from flaskapp.flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskapp.flaskblog import app, db, bcryp
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


@app.route("/")
def home():
    #posts = Post.query.all()
    page = request.args.get('page',1,type=int)
    print(f'The current page is {page}')
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=4)
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return "About"


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_password = bcryp.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcryp.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    print('Testing')
    return render_template('login.html', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_image(image_file):
    hex_text = secrets.token_hex(8)
    _, ext = os.path.splitext(image_file.filename)
    file_name = hex_text + ext
    image_path = os.path.join(app.root_path, 'static/profile_pics', file_name)

    output_size = (125, 125)
    i = Image.open(image_file)
    i.thumbnail(output_size)
    i.save(image_path)
    return file_name


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_path = save_image(form.picture.data)
            current_user.image_file = image_path
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("User account updated sucessfully", "success")
        redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', image_file=image_file, form=form)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', form=form)
    # return render_template('create_post.html', form=form)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def post(post_id):
    user_post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=user_post)


@app.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    user_post = Post.query.get_or_404(post_id)
    form = PostForm()
    if user_post.author != current_user:
        abort(403)
    if form.validate_on_submit():
        user_post.title = form.title.data
        user_post.content = form.content.data
        db.session.commit()
        return redirect(url_for('post' , post_id = user_post.id))
    elif request.method == 'GET':
        form.title.data = user_post.title
        form.content.data = user_post.content
        return render_template('create_post.html', form=form,update=True , post_id = user_post.id)


@app.route("/post/<int:post_id>/delete",methods=["GET", "POST"])
@login_required
def delete_post(post_id):
    print("Test")
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/user_post/<string:username>",methods=["GET", "POST"])
@login_required
def user_post(username):
    print("Test")
    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get('page', 1, type=int)
    print(page)
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=4)
    return render_template("user_post.html", posts=posts , user = user)



