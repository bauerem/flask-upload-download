from flask import Flask, send_file, render_template, request, make_response
from werkzeug.utils import secure_filename
import os
from random import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), 'static/files'
)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def is_allowed_filetype(filename):
    allowed_types = {'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_types

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['inputFile']
    #username = request.form['username']
    extension = file.filename.split('.')[-1]
    print(extension)
    token = int(random()*10**16)
    filename = str(token) + '.' + extension 
    if file and is_allowed_filetype( filename ):
        file.save(os.path.join(
            app.config['UPLOAD_FOLDER'],
            filename
        ))
    else:
        return {"fail": "fail! messed up file(name)"}
    response = render_template('index.html')
    #response = {"message": "success"}
    response = make_response(response)
    
    response.set_cookie('filename', filename)
    return response

@app.route('/download')
def download_file():
    path = os.path.join(
        app.config['UPLOAD_FOLDER'],
        request.cookies.get('filename')
    )
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)