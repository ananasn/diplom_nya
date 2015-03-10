import os
from flask import render_template, request, redirect, url_for, jsonify
from werkzeug import secure_filename

from app import app,ALLOWED_EXTENSIONS
from python_scripts import change_get_coordinates as cgc

@app.route('/')
@app.route('/index')
def index():
    def return_model():
        return("/static/model/m_start.js", "/static/model/model_1.js")
    return render_template("test7.html",title = 'Nyan', 
                            model_path = return_model()[0],
                            new_model_path = return_model()[1])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           

@app.route('/uploadajax', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = '.'.join(['upload_picture', file.filename.split('.')[1]])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            cgc.make_json_model('.'.join(\
                          ["./app/images/upload_pictures/upload_picture", file.filename.split('.')[1]]))
            path_to_image = os.path.join(app.config['UPLOAD_FOLDER'])
            return jsonify(name=filename)
        
