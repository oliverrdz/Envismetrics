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
from CV import CV

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

today = time.strftime("%Y-%m-%d", time.localtime())
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s line: %(lineno)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_DIR + '/logs/tnote-' + today + '.log')


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'txt', 'xlsx'}

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

@app.route("/hyd_elec")
def hyd_elec():
    notes = []
    return render_template('hyd_elec.html', notes=notes)

@app.route("/cv")
def cv():
    notes = []
    return render_template('cv.html', notes=notes)

@app.route('/upload', methods=['POST'])
def upload_file():

    try:
        print(request.form)
        module = request.form.get('module')

        print("module: " + module)
    except Exception as e:
        print(str(e))
        module = "None"

    if module == 'CV':
        step = request.form.get('step')
        if step == '1':
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

            sigma = request.form.get('sigma')
            print("sigma: " + str(sigma))
            c = CV(version=version, filepath=save_path, sigma=float(sigma))
            res = c.start1()
            return res
        elif step == '2':
            version = request.form.get('version')
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], version)

            sigma = request.form.get('sigma')
            method = 'Max'
            peak_range_top = request.form.get('peak_range_top')
            peak_range_bottom = request.form.get('peak_range_bottom')
            c = CV(version=version, filepath=save_path, sigma=float(sigma))
            res = c.start2(method=method, peak_range_top=peak_range_top, peak_range_bottom=peak_range_bottom)
            return res
        else:
            return {
                'status': False,
                'message': 'One or more files are not allowed.'
            }
    else:
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
        return jsonify(res)


@app.route('/outputs/<filename>')
def uploaded_file(filename):
    return send_from_directory('outputs', filename)

@app.route('/outputs/<version>/<filename>')
def uploaded_file2(filename, version):
    return send_from_directory('outputs/{}'.format(version), filename)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)