import os
from flask import render_template, request,\
redirect, url_for, jsonify, send_from_directory
from werkzeug import secure_filename

from app import app,ALLOWED_EXTENSIONS
from python_scripts import change_get_coordinates as cgc
from python_scripts import g_codes as gcode

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
            upload_file.params = cgc.make_json_model('.'.join(\
                          ["./app/images/upload_pictures/upload_picture",\
                          file.filename.split('.')[1]]))
            return jsonify(name=filename)
            
            
@app.route('/download', methods=['GET','POST'])
def download_file():
    if request.method == 'POST':
        g = gcode.Generator(upload_file.params[0], upload_file.params[2],\
                    upload_file.params[1], 3.0, 0.5, upload_file.params[3])
        gcode_list = g.generate()
        g.write(gcode_list)
        print(os.path.join(os.path.dirname(os.getcwd()),\
       'workspace', 'app', 'python_scripts'))
        return send_from_directory(os.path.join(os.path.dirname(os.getcwd()),\
       'workspace', 'app', 'python_scripts'), filename='g_codes.txt',as_attachment=True)