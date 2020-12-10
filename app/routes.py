from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user
from sqlalchemy.sql.functions import random
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, NewPostForm
from app.models import User, Post


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/category', methods=['GET', 'POST'])
def category():
    from .models import Post
    posts = Post.query.filter_by(category=Post.category).first()
    return render_template('category.html', posts=posts)


@app.route('/createPost', methods=['GET', 'POST'])
def createPost():
    form = NewPostForm()
    if form.validate_on_submit():
        flash('New post for category {}'.format(form.category.data))
        my_post = Post(title=form.title.data, category=form.category.data, body=form.body.data, author=current_user)
        db.session.add(my_post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('category'))
    return render_template('createPost.html', title='New post', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     return redirect(url_for('login'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('home'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
        return redirect((url_for('home')))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/')
@app.route("/quote")
def random_quote():
    quotes = [
        "You are but a lonely grasshopper in a big field",
        "Everyone has a plan, until they get punched.",
        "You miss 100% of the shots you don't take."]
    idx = random.randrange(len(quotes))
    return render_template('login.html', q=quotes[idx])


# @app.route('/')
# @app.route('/category')
# def the_posts():
#     user = {'username': 'User'}
#     posts = {
#         {'author': {'username': 'poster'}, 'body': {'This is a post'}},
#         {'author': {'username': 'poster'}, 'body': {'This is another post'}}
#     }
#     return render_template('category.html', title='Topic Page', user=user, posts=posts)


@app.route('/reset_db')
def reset_db():
    # if current_user.is_authenticated:
    #     return redirect(url_for('reset_db'))
    # clear all data from all tables
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        print('Clear table {}'.format(table))
        db.session.execute(table.delete())
    db.session.commit()

    u1 = User(username='SiR123', email='johnredcorn@gmail.com', password_hash='johnredcorn')
    u2 = User(username='lostCtrl', email='ctrl@gmail.com', password_hash='youandme')
    u3 = User(username='cadillacdrmz', email='nodestination@gmail.com', password_hash='noexpectations')

    db.session.add_all([u1, u2, u3])
    db.session.commit()

    now = datetime.utcnow()
    p1 = Post(category='Park', title='Park Sucks', author=u1, body='i hate this school, sos',
              timestamp=now + timedelta(seconds=1))
    p2 = Post(category='CHS', title='Where is the bathroom', author=u2, body='ive walked around for half of class, '
                                                                             'its a miracle i havent peed on myself',
              timestamp=now + timedelta(seconds=1))
    p3 = Post(category='CNS', title='I hate anatomy', author=u3, body='bones?????',
              timestamp=now + timedelta(seconds=1))
    db.session.add_all([p1, p2, p3])
    db.session.commit()

    return redirect(url_for('home'))
