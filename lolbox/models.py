# coding: utf-8
import time
from mongoengine import *
import os
from flask import current_app
from flask.ext.login import UserMixin
from app import login_manager

MONGODB_URI = os.environ.get("MONGODB_URI")
MONGODB_SETTINGS = {}
MONGODB_SETTINGS['db'] = MONGODB_URI.split("/")[-1]
MONGODB_SETTINGS['host'] = MONGODB_URI

connect(MONGODB_SETTINGS['db'], host=MONGODB_SETTINGS['host'])

class Post(Document):
    text = StringField(verbose_name=u"Текст")
    file_id = StringField(verbose_name=u"id файла")
    file_name = StringField(verbose_name=u"Название файла")
    time = FloatField(default=time.time, verbose_name=u"Время", help_text=u"Время создания поста")

class User(Document):
    username = StringField(verbose_name=u"Имя пользователя", unique=True)
    email = EmailField(unique=True, verbose_name=u"Email")
    password = StringField(verbose_name=u"Пароль")
    is_admin = BooleanField(verbose_name=u"Администратор?", default=False)
    timestamp = FloatField(default=time.time, verbose_name=u"Время регистрации")

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username

    def is_active(self):
        return True

    @staticmethod
    def verify_password(password_hash, password):
        return password == password_hash

@login_manager.user_loader
def load_user(id):
    return User.objects.get(username=id)
