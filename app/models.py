from datetime import datetime

from flask import url_for, render_template
from flask_login import login_manager, UserMixin, current_user, login_required
from flask_sqlalchemy import Model
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from app import db, login, app


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(64))
    title = db.Column(db.String(64))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # categories = db.relationship('CategoryToPost', backref='category', lazy='dynamic ')

    def __repr__(self):
        return '<Post {}>'.format(self.body)



class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    body = db.Column(db.String(140))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
            return '<Feedbacl {}>'.format(self.body)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    categories = Post.category.desc()



# # *//*
# class CategoryToPost(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
#
#     post = db.relationship('Post', backref='category', lazy=True)
#     category = db.relationship('Category', backref='post', lazy=True)
# //
