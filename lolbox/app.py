# coding: utf-8

from flask import Flask, render_template, request, abort
import time
from flask.ext.login import LoginManager, current_user

app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u"Сайт находится в закрытой разработке. Вход только по приглашениям."
login_manager.init_app(app)

@app.errorhandler(404)
def page_not_found(e):
        return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
        return render_template('500.html'), 500

@app.before_request
def check_login():
        if request.endpoint == 'admin.index':
                if current_user.is_authenticated and current_user.is_admin:
                                return
                abort(404)

from lolbox.models import *
@app.template_filter('id_to_username')
def id_to_username(id):
        return User.objects.get(id=str(id))['username']

from lolbox.views import home
from lolbox.views import auth
from lolbox.views import admin

app.register_blueprint(home.home)
app.register_blueprint(auth.auth)
app.register_blueprint(admin.admin_panel)
