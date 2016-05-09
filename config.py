import os

S3_LOCATION = 'lolbox.s3-website-us-east-1.amazonaws.com'
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")
S3_UPLOAD_DIRECTORY = 'uploads'
S3_BUCKET = 'lolbox'
MONGODB_URI = os.environ.get("MONGODB_URI")
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
SECRET_KEY = "FLASK_SECRET_KEY"
