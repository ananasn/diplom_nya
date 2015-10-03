# -*- coding: utf-8 -*-
import os
import base64

from werkzeug import secure_filename
from flask import render_template, request, url_for, \
    redirect, jsonify, send_from_directory, session
    
from app import app, ALLOWED_EXTENSIONS
from python_scripts import make_model as mm
from python_scripts import g_codes as gcode
from python_scripts import rshash


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title='Nyan')
    
@app.route('/editorpage')
def show_editor():
    picname = '/'.join(['images', session['hash_name']]) +'.jpg'
    return render_template("editor.html", title='Editor',
                           img_path=url_for('static', filename=picname))
            
@app.route('/uploadedited', methods=['POST'])
def upload_edited_pic():
    """Upload edited picture"""
    if request.method == 'POST':
        data = request.form['edited_file']
        # base64 string to picture
        data = data.replace('data:image/png;base64,', '')
        imgdata = base64.b64decode(data)
        name = 'app/static/images/' + session['hash_name'] + '_e' + '.jpg'
        with open(name, 'wb') as f:
            f.write(imgdata)
        #rebuild model
        session['model_name'] = session['hash_name'] + '_e' + '.stl'
        mm.make_stl_model(name.split('/')[-1])
        return jsonify(result=0)

@app.route('/model')
def model():
    return render_template("model_template.html", title="View Model",
                           model_path="/static/model/" + session['model_name'])
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
           
@app.route('/uploadajax', methods=['POST'])
def upload_file():
    """Upload picture and build model"""
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename): 
            hash_name = str(rshash.rs_hash(file.filename.split('.')[0]))
            if len(hash_name) >= 200:           #max value is 255 in linux
                hash_name = hash_name[:200]
                session['hash_name'] = hash_name
            else:
                session['hash_name'] = hash_name
            filename = '.'.join([hash_name, 'jpg'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            params = mm.make_stl_model('.'.join(\
                          [ hash_name, 'jpg']))
            session['params'] = []
            session['params'].extend(params[1:])
            session['model_name'] = params[4]
            return jsonify(name=0)
            
@app.route('/download', methods=['GET','POST'])
def download_file():
    """Download g-code"""
    if request.method == 'POST':
        gcodes_filename = '.'.join([session['params'][3].split('.')[0], 'txt'])
        gcodes_filename_path = './app/python_scripts/' + gcodes_filename
        name_of_image = '.'.join([session['hash_name'], 'jpg'])
        print(name_of_image)
        g = gcode.Generator(0.3, session['params'][2],          #offset, norm,
                            gcodes_filename_path,               #name_gcode_f
                            name_of_image)                      #name of image
        gcode_list = g.generate()
        g.write(gcode_list)
        return send_from_directory(
            os.path.join(os.path.dirname(os.getcwd()),
            'workspace', 'app', 'python_scripts'),
            filename=gcodes_filename, as_attachment=True
            )
       
@app.route('/download_model', methods=['GET', 'POST'])
def download_model():
    """Download stl-model"""
    if request.method == 'POST':
        return send_from_directory(
            os.path.join(os.path.dirname(os.getcwd()), 'workspace',
            'app', 'static', 'model'), filename=session['model_name'],
            as_attachment=True
            )