import time
from mongoengine import *
import os

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
