import pymongo
import os

MONGODB_URL = os.environ.get("MONGODB_URI")
client = pymongo.MongoClient(MONGODB_URL)
db = client.get_default_database()

def get_coll(coll):
        return db[coll]
