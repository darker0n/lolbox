import os
from flask import *
from flask.ext.bootstrap import Bootstrap
import pymongo
import collections

app = Flask(__name__)
bootstrap = Bootstrap(app)

MONGO_URL = os.environ.get("MONGODB_URL")
client = pymongo.MongoClient(MONGODB_URL)

db = client.get_default_database()

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500

@app.route('/ticket/<int:number>')
def ticket(number):
        collection = db['tickets']
        ticket = collection.find_one({"number": number})
        print ticket
        return render_template('ticket.html', ticket=ticket)

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
