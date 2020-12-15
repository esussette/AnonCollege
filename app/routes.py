from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.sql.functions import random
from werkzeug.urls import url_parse


from app import app, db
from app.forms import LoginForm, RegistrationForm, NewPostForm, FeedbackForm
from app.models import User, Post, Feedback


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/category', methods=['GET', 'POST'])
def category():
    from .models import Post
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('category.html', posts=posts)


@app.route('/', methods=['GET', 'POST'])
@app.route('/academics', methods=['GET', 'POST'])
def academics():
    from .models import Post
    posts = Post.query.filter_by(category=Post.category).first()
    # posts = Post.query.filter_by(category='Academic')
    return render_template('academics.html', posts=posts)

@app.route('/', methods=['GET', 'POST'])
@app.route('/campusevents', methods=['GET', 'POST'])
def campusevents():
    from .models import Post
    posts = Post.query.filter_by(category=Post.category).first()
    # posts = Post.query.filter_by(category='Academic')
    return render_template('campusevents.html', posts=posts)


@app.route('/createPost', methods=['GET', 'POST'])
def createPost():
    form = NewPostForm()
    if request.method == 'GET':
        form.category.default = 'Academics'
        form.process()
    elif form.validate_on_submit():
        flash('New post for category {}'.format(form.category.data))
        my_post = Post(title=form.title.data, category=form.category.data, body=form.body.data, author=current_user)
        db.session.add(my_post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('category'))
    return render_template('createPost.html', title='New post', form=form)


@app.route('/sendFeedback', methods=['GET', 'POST'])
def sendFeedback():
    form = FeedbackForm()
    if form.validate_on_submit():
        flash('Feedback sent. Thank you for your submission!')
        the_form = Feedback(name=form.name.data, email=form.email.data, body=form.body.data)
        db.session.add(the_form)
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('feedback.html', title='New feedback form', form=form)


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
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    posts = [
        {'author': user, 'body': 'Test post #2'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)



















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
                                                                             'please help',
              timestamp=now + timedelta(seconds=1))
    p3 = Post(category='CNS', title='I hate anatomy', author=u3, body='bones?????',
              timestamp=now + timedelta(seconds=1))
    db.session.add_all([p1, p2, p3])
    db.session.commit()

    # c2p1 = CategoryToPost(post=p1, category=p1.category)
    # db.session.add_all([c2p1])
    # db.session.commit()

    return redirect(url_for('home'))
