from flask import Blueprint, render_template
from lolbox.db import get_coll
import os

home = Blueprint('home', __name__)

@home.route('/', methods=['GET'])
def homepage():
        return render_template('index.html', topics=[x for x in get_coll("topics").find()])

@home.route('/', methods=['POST'])
def new_topic():
        coll = get_coll("topics")
        name = request.form["text"]
        coll.insert({"number": coll.count() + 1,
                     "name": name,
                     "posts": []})
        return redirect(request.path)

@home.route('/rules')
def rules():
        return render_template('rules.html')
