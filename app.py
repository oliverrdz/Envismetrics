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
import hashlib
import shutil
from config import *

app = Flask(__name__)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

today = time.strftime("%Y-%m-%d", time.localtime())
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s line: %(lineno)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=BASE_DIR + '/logs/tnote-' + today + '.log')

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
    return render_template('m1_hyd_elec.html', notes=notes)

@app.route("/cv")
def cv():
    notes = []
    return render_template('m2_cv.html', notes=notes)


def calculate_file_md5(file_path):
    """计算文件的 MD5 哈希值"""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        # 以二进制方式读取文件并更新哈希值
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def check_if_file_exists(md5_hash):
    folder_files = os.listdir(UPLOAD_FOLDER)
    for existing_file in folder_files:
        existing_file_name, _ = os.path.splitext(existing_file)
        if existing_file_name == md5_hash:
            print("File already exists:", existing_file)
            return True, os.path.join(UPLOAD_FOLDER, existing_file)
    return False, ''


def save_files(files, save_path, version):
    """
    :param files:
    :return: files info path

    list of file info: {
        'version': version,
        'filename': filename, # 用户上传的原始文件名
        'md5': md5,           # 将文件名
    }
    """

    info = []

    # 先存到临时文件，再计算每一个 md5 值。以此判断避免重复占用空间。
    for file in files:
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            to_file_tmp = os.path.join(TMP_FOLDER, filename)
            file.save(to_file_tmp)
            print("uploaded to " + to_file_tmp)

            md5_hash = calculate_file_md5(to_file_tmp)

            existed, existed_filename =  check_if_file_exists(md5_hash)
            if not existed:
                extension = filename.rsplit('.', 1)[1].lower()
                existed_filename = os.path.join(UPLOAD_FOLDER, "{}.{}".format(md5_hash, extension))
                file.save(existed_filename)
                shutil.move(to_file_tmp, existed_filename)
                print("saved to " + existed_filename)

            info.append({
                'version': version,
                'filename': filename,
                'md5': md5_hash,
                'existed_filename': existed_filename,
            })
    to_file_info = os.path.join(save_path, "fileinfo_{}.json".format(version))
    with open(to_file_info, 'w') as f:
        f.write(json.dumps(info))
    return to_file_info

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
            files_info = save_files(files, save_path, version)

            sigma = request.form.get('sigma')
            print("sigma: " + str(sigma))
            c = CV(version=version, files_info=files_info, sigma=float(sigma))
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
        files_info = save_files(files, save_path, version)

        h = HDV(version=version, files_info=files_info)
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