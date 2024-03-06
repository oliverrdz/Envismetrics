from werkzeug.utils import secure_filename
from flask import Flask, render_template, send_from_directory, jsonify, request, redirect
import time
import datetime
import logging
import os
import json
import configparser
from datetime import datetime
from HDV import HDV

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

today = time.strftime("%Y-%m-%d", time.localtime())
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s line: %(lineno)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_DIR + '/logs/tnote-' + today + '.log')


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'txt', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/demo")
def demo():
    notes = []
    return render_template('demo.html', notes=notes)

@app.route("/")
def index():
    notes = []
    return render_template('index.html', notes=notes)


@app.route('/upload', methods=['POST'])
def upload_file():
    version = "version_" + datetime.now().strftime("%m%d_%H%M%S")
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], version)
    if not os.path.exists(save_path):
        os.makedirs(save_path, exist_ok=True)

    if 'files[]' not in request.files:
        return 'No file part'

    files = request.files.getlist('files[]')

    for file in files:
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            to_file = os.path.join(save_path, filename)
            file.save(to_file)
            print("save to " + to_file)

    h = HDV(version=version, filepath=save_path)
    res = h.start()
    return jsonify({
        'message': 'Files uploaded successfully',
        'file1': res['file1'],
        'file2': res['file2'],
    })


@app.route('/outputs/<filename>')
def uploaded_file(filename):
    return send_from_directory('outputs', filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)