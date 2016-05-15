# coding: utf-8
from flask import Blueprint, render_template, current_app, request, flash, redirect
from lolbox.db import get_coll
from wtforms.validators import *
import datetime
from lolbox.tools import s3_upload
from flask_wtf import Form
from flask_wtf.file import FileField

posts = Blueprint('posts', __name__)

class UploadForm(Form):
        file = FileField('File')

@posts.route('/topic/<int:number>', methods=['GET', 'POST'])
def ticket(number):
        coll = get_coll("topics")
        topic = coll.find_one({"number": number})
	form = UploadForm()

    	if form.validate_on_submit():
        	output = s3_upload(form.file, current_app.config)
                result = coll.update_one({"number": number},
                                         {"$pushAll":
                                          {"posts": [{"text":request.form["text"],
                                                      "file_id": output,
                                                      "file_name": form.file.data.filename,
                                                      "time": datetime.datetime.now()}]}})
                flash(u'пост залит.')
                return redirect(request.path)
        return render_template('topic.html', form=form, topic=topic)
