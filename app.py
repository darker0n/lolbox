# coding: utf-8
import os
from flask import Flask, render_template, redirect, url_for, flash, request, send_from_directory
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import *
from werkzeug import secure_filename
import datetime
import pymongo
import collections
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pashaandmisha'

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024
MONGODB_URL = os.environ.get("MONGODB_URI")
client = pymongo.MongoClient(MONGODB_URL)
db = client.get_default_database()

def get_coll(coll):
        return db[coll]

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500

@app.route('/uploads/<file_id>')
def uploaded_file(file_id):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               file_id)

@app.route('/topic/<int:number>', methods=['GET', 'POST'])
def ticket(number):
        coll = get_coll("topics")
        topic = coll.find_one({"number": number})

        if request.method == 'POST':
		file = request.files['file']
        	if file and allowed_file(file.filename):
            		extension = os.path.splitext(secure_filename(file.filename))[1]
                        file_name = secure_filename(file.filename)
                        file_id = len([name for name in os.listdir(app.config['UPLOAD_FOLDER']) if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], name))]) + 1
                        target = '{0}{1}'.format(str(file_id), extension)
            		file.save(os.path.join(app.config['UPLOAD_FOLDER'], target))
                result = coll.update_one({"number": number},
                                               {"$pushAll":
                                                {"posts": [{"text":request.form["text"],
                                                            "file_id": target,
                                                            "file_name": file_name,
                                                            "time": datetime.datetime.now()}]}})
                flash(u'пост залит.')
                return redirect(request.path)
        return render_template('topic.html', topic=topic)

@app.route('/')
def homepage():
        return render_template('index.html', topics=[x for x in get_coll('topics').find()])

if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
