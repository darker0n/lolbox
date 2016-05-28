from flask import Blueprint, render_template, request, redirect, abort, url_for
from lolbox.models import *
from lolbox.app import app
from flask.ext.login import login_user, logout_user, login_required, current_user
from flask.ext.superadmin import *

admin_panel = Blueprint('admin_panel', __name__)

class AuthMixin(object):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False

    def _handle_view(self, name, *args, **kwargs):
        if not self.is_accessible():
            abort(404)

class UserModel(AuthMixin, model.ModelAdmin):
    list_display = ('username','email')

class PostModel(AuthMixin, model.ModelAdmin):
    list_display = ('text',)

admin = Admin(app, 'lolbox')

admin.register(User, UserModel)
admin.register(Post, PostModel)
