from flask import *
from flask.ext.bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
            return render_template('500.html'), 500

@app.route('/')
def homepage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
