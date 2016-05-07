# coding: utf-8
import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import TextAreaField, SubmitField
from wtforms.validators import *
import pymongo
import collections

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pashaandmisha'
bootstrap = Bootstrap(app)

MONGODB_URL = os.environ.get("MONGODB_URI")
client = pymongo.MongoClient(MONGODB_URL)

db = client.get_default_database()

class NewAnswerForm(Form):
        answer = TextAreaField(u'напиши сюда свой ответ, чтобы его увидели другие.', validators=[Required()])
        submit = SubmitField(u'отправить.')

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500

@app.route('/ticket/<int:number>', methods=['GET', 'POST'])
def ticket(number):
        form = NewAnswerForm()
        collection = db['tickets']
        ticket = collection.find_one({"number": number})

        if request.method == 'POST' and form.validate():
                result = collection.update_one({"number": number}, {"$pushAll": {"answers": [form.answer.data]}})
                flash(u'спс. да хранит тебя Господь.')
                return redirect('/ticket/' + str(number))
        return render_template('ticket.html', ticket=ticket, form=form)

@app.route('/')
def homepage():
        collection = db['tickets']
        tickets = []
        for ticket in collection.find():
                tickets.append(ticket)
        return render_template('index.html', tickets=sorted(tickets, key=lambda k: k["number"]))

if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
