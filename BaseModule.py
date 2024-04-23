import os
import json
import re
import pandas as pd

def reorder(filename):
    match = re.search(r'(\d+)rpm', filename)
    if match:
        return int(match.group(1))
    else:
        # Handle files without RPM values
        return -1  # You can use any default value or treatment

def extract_rpm(filename):
    pattern = r'(?:^|_)(\d+rpm)\.'
    match = re.search(pattern, filename)
    if match:
        return match.group(1)
    else:
        return None

def check_files(files):
    for f in files:
        ext = f.split('.')[-1].lower()
        if ext not in ['xlsx', 'txt']:
            return False
    return True

class BaseModule(object):
    def __init__(self, version):
        self.version = version
        self.files_info = os.path.join('uploads', version, 'fileinfo.json')
        self.datapath = os.path.join('outputs', self.version)

        if not os.path.exists(self.datapath):
            os.mkdir(self.datapath)

        # 该文件用于存放用户的输入，和每一步的结果
        self.res_data = self.read_result_data()


    def read_result_data(self):
        data_file = os.path.join(self.datapath, 'data.json')
        if os.path.exists(data_file):
            data = json.loads(open(data_file, 'r').read())
        else:
            data = {'version': self.version}
        return data

    def save_result_data(self, data):
        data_file = os.path.join(self.datapath, 'data.json')
        with open(data_file, "w") as json_file:
            json.dump(data, json_file, indent=4)
            print("saved to: {}".format(data_file))


    def read_data(self):
        """
        TODO 尚未完成
        :return:
        """
        with open(self.files_info, 'r') as f:
            info_list = json.loads(f.read())

        files = []
        real_file_path = {}
        for info in info_list:
            # input your file name here and switch rpm in to %d
            f = info['filename']
            file = info['existed_filename']
            if not os.path.isfile(file):
                continue
            files.append(f)
            real_file_path[f] = file
        files = sorted(files, key=reorder)

        data = []
        for f in files:
            file = real_file_path[f]
            if not os.path.isfile(file):
                continue
            print(f)
            if file.endswith(".xlsx"):
                csv_file = file + ".csv"
                if os.path.exists(csv_file):
                    df = pd.read_csv(csv_file, sep=',')
                else:
                    data0 = pd.ExcelFile(file)
                    df = data0.parse('Sheet1')
                    df.to_csv(csv_file, sep=',', index=False)
                    print("saved csv file to {}".format(csv_file))
            elif file.endswith(".txt"):
                df = pd.read_csv(file, delimiter=';')
            elif file.endswith(".csv"):
                df = pd.read_csv(file, delimiter=',')
            else:
                df = None
            data.append({
                'filename': f,
                'df': df,
            })
        print("data: ", len(data))
        return data