# coding: utf-8
import time
from mongoengine import *
import os
from flask import current_app
from flask.ext.login import UserMixin, AnonymousUserMixin
from app import login_manager

MONGODB_URI = os.environ.get("MONGODB_URI")
MONGODB_SETTINGS = {}
MONGODB_SETTINGS['db'] = MONGODB_URI.split("/")[-1]
MONGODB_SETTINGS['host'] = MONGODB_URI

connect(MONGODB_SETTINGS['db'], host=MONGODB_SETTINGS['host'])

class Post(Document):
    text = StringField(verbose_name=u"текст")
    file_id = StringField(verbose_name=u"id файла", help_text=u"id файла, данное при загрузки в S3")
    file_name = StringField(verbose_name=u"файл", help_text=u"имя файла")
    time = FloatField(default=time.time, verbose_name=u"время", help_text=u"время создания поста")
    author = StringField(verbose_name=u"автор", help_text=u"id автора поста")

class User(Document):
    username = StringField(verbose_name=u"никнейм", unique=True)
    email = EmailField(unique=True, verbose_name=u"email")
    password = StringField(verbose_name=u"пароль")
    is_admin = BooleanField(verbose_name=u"администратор?", default=False)
    member_since = FloatField(default=time.time, verbose_name=u"время регистрации")
    location = StringField(verbose_name=u"месторасположение")
    name = StringField(verbose_name=u"имя")

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True

    @staticmethod
    def verify_password(password_hash, password):
        return password == password_hash

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(id):
    return User.objects.get(id=id)
