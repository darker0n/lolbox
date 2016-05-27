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
    text = StringField(max_lenght=100)
    file_id = StringField()
    file_name = StringField()
    time = FloatField(default=time.time)

class User(Document):
    username = StringField(max_lenght=64)
    email = EmailField()
    password = StringField()

    def is_authenticated(self):
        return True

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
