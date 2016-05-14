from flask import Flask, render_template

app = Flask(__name__)
app.config.from_object('config')

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500

from lolbox.views import home
from lolbox.views import posts

app.register_blueprint(home.home)
app.register_blueprint(posts.posts)
