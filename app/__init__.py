from os import urandom
from flask import Flask

UPLOAD_FOLDER = "./app/static/images"
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = urandom(24)
from app import view