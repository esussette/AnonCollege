from random import random

from flask import render_template

from app import app


@app.route("/quote")
def random_quote():
    quotes = [
        "You are but a lonely grasshopper in a big field",
        "Everyone has a plan, until they get punched.",
        "You miss 100% of the shots you don't take."]
    idx = random.randrange(len(quotes))
    return render_template('login.html', q=quotes[idx])
