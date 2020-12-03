from random import random
from flask import render_template
from app import app

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
#Example of routing to a page of posts - this route name is a placeholder bc we
#have not decided on those specifics yet
def the_posts():
    user = {'username': 'User'}
    posts = {
        {
            'author': {'username': 'poster'}
            'body' : 'This is a post'
        },
        {
            'author': {'username': 'poster'},
            'body': 'This is another post'
        }
    }
    return render_template('topic.html', title='Topic Page', user=user, posts=posts)

