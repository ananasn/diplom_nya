from flask import Flask

UPLOAD_FOLDER = "./app/images/upload_pictures"
ALLOWED_EXTENSIONS = set(['jpg', 'png', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from app import view