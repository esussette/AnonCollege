from datetime import datetime, timedelta

from flask import render_template, redirect, url_for, flash, request, g
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.sql.functions import random
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, NewPostForm, FeedbackForm, EditProfileForm, EmptyForm
from app.models import User, Post, Feedback


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
@app.route('/category', methods=['GET', 'POST'])
def category():
    from .models import Post
    posts = current_user.followed_posts().all()
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    return render_template('category.html', posts=posts.items)


@app.route('/', methods=['GET', 'POST'])
@app.route('/explore', methods=['GET', 'POST'])
def explore():
    from .models import Post
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    return render_template('category.html', posts=posts.items)
    return render_template('explore.html', title='Explore', posts=posts)



@app.route('/', methods=['GET', 'POST'])
@app.route('/academics', methods=['GET', 'POST'])
def academics():
    from .models import Post
    posts = Post.query.filter_by(category=Post.category).first()
    # posts = Post.query.filter_by(category='Academic')
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    return render_template('academics.html', posts=posts.items)


@app.route('/', methods=['GET', 'POST'])
@app.route('/campusevents', methods=['GET', 'POST'])
def campusevents():
    from .models import Post
    posts = Post.query.filter_by(category=Post.category).first()
    # posts = Post.query.filter_by(category='Academic')
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, app.config['POSTS_PER_PAGE'], False)

    return render_template('campusevents.html', posts=posts.items)


@app.route('/createPost', methods=['GET', 'POST'])
@login_required
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
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts, form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    else:
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))


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
    u4 = User(username='angryspice', email='angry@gmail.com', password_hash='beautiful')
    u5 = User(username='hearttoheart', email='baby@gmail.com', password_hash='please')
    u6 = User(username='hello', email='nonono@gmail.com', password_hash='dontjudgeme')

    db.session.add_all([u1, u2, u3, u4, u5, u6])
    db.session.commit()

    now = datetime.utcnow()
    p1 = Post(category='Park', title='Park Sucks', author=u1, body='i hate this school, sos',
              timestamp=now + timedelta(seconds=1))
    p2 = Post(category='CHS', title='Where is the bathroom', author=u2, body='ive walked around for half of class, '
                                                                             'please help',
              timestamp=now + timedelta(seconds=1))
    p3 = Post(category='CNS', title='I hate anatomy', author=u3, body='bones?????',
              timestamp=now + timedelta(seconds=1))
    p4 = Post(category='Academics', title='Finals Week SOS', author=u4, body='this finals week is driving me crazy',
              timestamp=now + timedelta(seconds=1))
    p5 = Post(category='Academics', title='Winter Class', author=u5, body='does anyone have any winter courses recs??',
              timestamp=now + timedelta(seconds=1))
    p6 = Post(category='Academics', title='Spring 2020', author=u6, body='When does the next semester start does '
                                                                         'anyone know',
              timestamp=now + timedelta(seconds=1))
    db.session.add_all([p1, p2, p3, p4, p5, p6])
    db.session.commit()

    # c2p1 = CategoryToPost(post=p1, category=p1.category)
    # db.session.add_all([c2p1])
    # db.session.commit()

    return redirect(url_for('home'))
