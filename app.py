# coding: utf-8
import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from wtforms.validators import *
from werkzeug import secure_filename
import datetime
import pymongo
import collections
import hashlib
from tools import s3_upload
from flask_wtf import Form
from flask_wtf.file import FileField
import boto

app = Flask(__name__)
app.config.from_object('config')

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

class UploadForm(Form):
        file = FileField('File')

@app.route('/topic/<int:number>', methods=['GET', 'POST'])
def ticket(number):
        coll = get_coll("topics")
        topic = coll.find_one({"number": number})
	form = UploadForm()

    	if form.validate_on_submit():
        	output = s3_upload(form.file, app.config)
                result = coll.update_one({"number": number},
                                               {"$pushAll":
                                               {"posts": [{"text":request.form["text"],
                                                           "file_id": output,
                                                            "file_name": form.file.data.filename,
                                                            "time": datetime.datetime.now()}]}})
                flash(u'пост залит.')
                return redirect(request.path)
        return render_template('topic.html', form=form, topic=topic)

@app.route('/')
def homepage():
        return render_template('index.html', topics=[x for x in get_coll("topics").find()])

@app.route('/', methods=['POST'])
def new_topic():
        coll = get_coll("topics")
        name = request.form["text"]
        coll.insert({"number": coll.count() + 1,
                     "name": name,
                     "posts": []})
        return redirect(request.path)

if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run()
