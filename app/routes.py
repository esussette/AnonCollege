from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user
from sqlalchemy.sql.functions import random, current_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, NewPostForm
from app.models import User


@app.route('/')
@app.route('/home')
def homepage():
    return render_template('index.html')


@app.route('/category')
def category():
    return render_template('category.html')


@app.route('/createPost')
def createPost():
    form = NewPostForm()
    if form.validate_on_submit():
        flash('New post for category {}'.format(form.Artist.data))
        my_post = NewPostForm(title=form.title.data, description=form.description.data)
        db.session.add(my_post)
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('createPost.html', title='New artists', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/')
@app.route("/quote")
def random_quote():
    quotes = [
        "You are but a lonely grasshopper in a big field",
        "Everyone has a plan, until they get punched.",
        "You miss 100% of the shots you don't take."]
    idx = random.randrange(len(quotes))
    return render_template('login.html', q=quotes[idx])


@app.route('/')
@app.route('/topic')
# Example of routing to a page of posts - this route name is a placeholder bc we
# have not decided on those specifics yet
def the_posts():
    user = {'username': 'User'}
    posts = {
        {'author': {'username': 'poster'}, 'body': {'This is a post'}},
        {'author': {'username': 'poster'}, 'body': {'This is another post'}}
    }
    return render_template('topic.html', title='Topic Page', user=user, posts=posts)
