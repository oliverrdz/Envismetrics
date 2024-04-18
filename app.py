from werkzeug.utils import secure_filename
from flask import Flask, render_template, send_from_directory, jsonify, request, redirect, send_file, abort
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
import threading
import traceback

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
    data = {}
    return render_template('index.html', data=data)

# Menu 1
@app.route("/hyd_elec")
def hyd_elec():
    data = {}
    data['version'] = ''
    data['step'] = ''
    return render_template('m1_hyd_elec.html', data=data)

@app.route("/hyd_elec/<version>")
def hyd_elec2(version=None):
    data = {
        'version': version
    }
    module = 'HDV'
    step = int(request.args.get('step', '2'))
    step = 2 if step < 2 else step
    data_path = os.path.join('outputs', version)
    if not os.path.exists(data_path):
        abort(404)

    data_file = os.path.join(data_path, 'data.json')

    if os.path.exists(data_file):
        try:
            data = json.loads(open(data_file).read())
            data = data[module]
            print('---')
            print(data)
            # 检查状态
            kk = 'form{}'.format(step - 1)  # Step k 要用到 Form k-1 的结果。
            status = data[kk]['status']
        except Exception as e:
            traceback.print_exc()
            data = {}
            status = 'processing'
    else:
        traceback.print_exc()
        data = {}
        status = 'processing'

    data['processing_display'] = 'none' if status == 'done' else 'block'
    data['form1_processing_display'] = 'block' if status == 'done' else 'none'
    data['version'] = version
    data['step'] = step

    return render_template('m1_hyd_elec_step2.html', data=data)

# Menu 2
@app.route("/cv")
def cv():
    data = CV.demo_data()
    data['version'] = ''
    return render_template('m2_cv.html', data=data)

@app.route("/cv/<version>")
def cv2(version=None):
    data = {
        'version': version
    }
    module = 'CV'
    step = int(request.args.get('step', '1'))
    data_file = os.path.join('outputs', version, 'data.json')
    if os.path.exists(data_file):
        data = json.loads(open(data_file).read())
        print('---')
        print(data)

        # 检查状态
        kk = 'form{}'.format(step-1) # Step k 要用到 Form k-1 的结果。
        if data[module][kk]['status'] == 'processing':
            is_processing = True
        else:
            is_processing = False

        # update_display
        for i in [1, 2, 3]:
            k = 'form{}'.format(i)
            if k not in data[module].keys():
                data[module][k] = {}
            if i == step and not is_processing:
                data[module][k]['display'] = 'block'
            else:
                data[module][k]['display'] = 'none'

        data[module]['processing_display'] = 'block' if is_processing else 'none'
        data['version'] = version
        data['step'] = step
    else:
        abort(404)
    # print(json.dumps(data))

    return render_template('m2_cv.html', data=data)

@app.route("/check/<module>/<version>")
def check(module, version):
    step = int(request.args.get('step', '1'))
    module = module.upper()

    print("version", version)
    print("module", module)
    print("step", step)

    data_file = os.path.join('outputs', version, 'data.json')
    if not os.path.exists(data_file):
        data = {'result': 'file not exists'}
        return jsonify(data)

    data = json.loads(open(data_file).read())

    if module not in data.keys():
        data = {'result': 'module not exists'}
        return jsonify(data)

    if module == 'CV':
        f = 'form{}'.format(step-1)
        if data[module][f]['status'] == 'done':
            data = {'result': 'done'}
            return jsonify(data)
    elif module == 'HDV':
        f = 'form1'
        if f not in data[module].keys():
            data = {'result': 'form1 not exists'}
            return jsonify(data)
        if data[module][f]['status'] == 'done':
            data = {'result': 'done'}
            return jsonify(data)

    data = {'result': 'processing'}
    return jsonify(data)

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

            data_path = os.path.join('outputs', version)
            if not os.path.exists(data_path):
                os.makedirs(data_path, exist_ok=True)
            data_file = os.path.join(data_path, 'data.json')
            if not os.path.exists(data_file):
                data = CV.demo_data()
                data['version'] = version

                with open(data_file, 'w') as f:
                    json.dump(data, f)

            if 'files[]' not in request.files:
                return 'No file part'

            files = request.files.getlist('files[]')
            files_info = save_files(files, save_path, version)

            sigma = request.form.get('sigma')
            print("sigma: " + str(sigma))

            user_input = {
                'version': version,
                'module': module,
                'step': step,
                'data': {
                    'files_info': files_info,
                    'sigma': float(sigma)
                }
            }
            # 创建子线程，并启动后台任务
            background_thread = threading.Thread(target=background_task, args=(user_input,))
            background_thread.start()

            return jsonify({
                'status': True,
                'message': 'Success, please wait.',
                'version': version
            })
        elif step == '2':
            version = request.form.get('version')
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], version)
            files_info = os.path.join(save_path, "fileinfo_{}.json".format(version))

            sigma = request.form.get('sigma')
            method = 'Max'
            peak_range_top = request.form.get('peak_range_top')
            peak_range_bottom = request.form.get('peak_range_bottom')

            user_input = {
                'version': version,
                'module': module,
                'step': step,
                'data': {
                    'files_info': files_info,
                    'sigma': float(sigma),
                    'method': method,
                    'peak_range_top': peak_range_top,
                    'peak_range_bottom': peak_range_bottom
                }
            }
            # 创建子线程，并启动后台任务
            background_thread = threading.Thread(target=background_task, args=(user_input,))
            background_thread.start()

            return {
                'status': True,
                'message': 'Success, please wait.',
                'version': version
            }
        else:
            return jsonify({
                'status': False,
                'message': 'One or more files are not allowed.'
            })
    elif module == 'HDV':
        step = request.form.get('step', '1')
        version = "version_" + datetime.now().strftime("%m%d_%H%M%S")
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], version)
        if not os.path.exists(save_path):
            os.makedirs(save_path, exist_ok=True)

        if 'files[]' not in request.files:
            return 'No file part'

        files = request.files.getlist('files[]')
        files_info = save_files(files, save_path, version)

        user_input = {
            'version': version,
            'module': module,
            'step': step,
            'data': {
                'files_info': files_info,
                'sigma': float(10)
            }
        }
        # 创建子线程，并启动后台任务
        background_thread = threading.Thread(target=background_task, args=(user_input,))
        background_thread.start()

        return jsonify({
            'status': True,
            'message': 'Success, please wait.',
            'version': version
        })


@app.route('/outputs/<filename>')
def uploaded_file(filename):
    return send_from_directory('outputs', filename)

@app.route('/outputs/<version>/<filename>')
def uploaded_file2(filename, version):
    return send_from_directory('outputs/{}'.format(version), filename)

@app.route('/files/<filename>')
def files(filename):
    # return send_from_directory('data/example_files', filename)
    return send_file('data/example_files/{}'.format(filename) , as_attachment=True)


def background_task(param):
    print("Background task started with parameter:", param)

    if param['module'] == 'CV':
        if param['step'] == '1':
            d = param['data']
            c = CV(version=param['version'], files_info=d['files_info'], sigma=d['sigma'])
            c.start1()
        elif param['step'] == '2':
            d = param['data']
            c = CV(version=param['version'], files_info=d['files_info'], sigma=d['sigma'])
            c.start2(method=d['method'], peak_range_top=d['peak_range_top'], peak_range_bottom=d['peak_range_bottom'])
    elif param['module'] == 'HDV':
        d = param['data']
        h = HDV(version=param['version'], files_info=d['files_info'])
        h.start()

    print("Background task completed")


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=8080)