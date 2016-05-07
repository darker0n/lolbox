# coding: utf-8
import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import *
import pymongo
import collections

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pashaandmisha'

MONGODB_URL = os.environ.get("MONGODB_URI")
client = pymongo.MongoClient(MONGODB_URL)
db = client.get_default_database()

def get_coll(coll):
        return db[coll]

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500

@app.route('/topic/<int:number>', methods=['GET', 'POST'])
def ticket(number):
        coll = get_coll("topics")
        topic = coll.find_one({"number": number})

        if request.method == 'POST':
                result = coll.update_one({"number": number},
                                               {"$pushAll":
                                                {"comments": [request.form["text"]]}})
                flash(u'спс. да хранит тебя Господь.')
                return redirect(request.path)
        return render_template('topic.html', topic=topic)

@app.route('/')
def homepage():
        return render_template('index.html', topics=[x for x in get_coll('topics').find()])

if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
