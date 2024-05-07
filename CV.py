import os as os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from sklearn.linear_model import LinearRegression
import math
import re
import json
from config import *
from BaseModule import BaseModule

def extract_rpm(filename):
    pattern = r'(?:^|_)(\d+rpm)\.'
    match = re.search(pattern, filename)
    if match:
        return match.group(1)
    else:
        return None


def extract_mvs(filename):
    pattern = r'(?:^|_)(\d+mVs)_CV\.'
    match = re.search(pattern, filename)
    if match:
        return match.group(1)
    else:
        return None


def check_files(files):
    for f in files:
        ext = f.split('.')[-1].lower()
        if ext not in ALLOWED_EXTENSIONS:  # ['xlsx', 'txt', 'csv']
            return False
    return True


def find_max(x, y, start, end):
    ma = -1
    xx = -1
    yy = -1
    for i in range(len(x)):
        if x[i] >= start and x[i] <= end:
            if y[i] > ma:
                ma = y[i]
                xx = x[i]
                yy = y[i]
    return xx, yy


def find_min(x, y, start, end):
    mi = 10000
    xx = -1
    yy = -1
    for i in range(len(x)):
        if x[i] >= start and x[i] <= end:
            if y[i] < mi:
                mi = y[i]
                xx = x[i]
                yy = y[i]
    return xx, yy


def find_y(x, y, xi):
    for i in range(len(x)):
        if x[i] == xi:
            return y[i]
    return -1


def extract_peak_range(str_peak_range):
    res = []
    arr = str_peak_range.strip().replace(" ", "").split('),(')
    for a in arr:
        start = a.split(",")[0].replace("(", "").replace(")", "").strip()
        end = a.split(",")[1].replace("(", "").replace(")", "").strip()
        res.append((float(start), float(end)))
    # # 使用正则表达式匹配坐标
    # pattern = r'\((-?\d+(\.\d+)?),(-?\d+(\.\d+)?)\)'
    # matches = re.findall(pattern, str(str_peak_range))
    #
    # # 提取匹配到的坐标
    # coordinates = [(float(match[0]), float(match[2])) for match in matches]
    # return coordinates
    return res


def separater(x, y, left, right):
    upperx = []
    lowerx = []
    uppery = []
    lowery = []

    x = x.tolist()  # Convert Int64Index to list
    y = y.tolist()  # Convert Int64Index to list

    boundary_l = x.index(left)
    boundary_r = x.index(right)

    if boundary_r < boundary_l:
        upperx = x[boundary_l:] + x[:boundary_r + 1]
        uppery = y[boundary_l:] + y[:boundary_r + 1]
        lowerx = x[boundary_r:boundary_l + 1]
        lowery = y[boundary_r:boundary_l + 1]
    else:
        upperx = x[boundary_l:boundary_r + 1]
        uppery = y[boundary_l:boundary_r + 1]
        lowerx = x[boundary_r:] + x[:boundary_l + 1]
        lowery = y[boundary_r:] + y[:boundary_l + 1]

    return upperx, lowerx, uppery, lowery


def reorder(filename):
    match = re.search(r'(\d+)mVs', filename)
    if match:
        return int(match.group(1))
    else:
        # Handle files without RPM values
        return -1  # You can use any default value or treatment


def filter_files(files):
    res = []
    for f in files:
        ext = f.split('.')[-1].lower()
        if ext in ALLOWED_EXTENSIONS:
            res.append(f)
    return res


class CV(BaseModule):
    def __init__(self, version, files_info):
        super().__init__(version)
        self.version = version
        self.files_info = files_info
        self.savepath = 'outputs/' + version
        if not os.path.exists(self.savepath):
            os.makedirs(self.savepath)


    """
    @staticmethod
    def demo_data():
        return {
            "CV": {
                "form1": {
                    "status": 'processing',
                    "input": {
                        "uploaded_files": [],
                        "sigma": 10
                    },
                    "output": {
                        "file1": "/static/imgs/Picture1.png",
                        "file2": "/static/imgs/Picture1.png"
                    },
                    "display": "block"
                },
                "form2": {
                    "status": 'processing',
                    "input": {
                        "peak_range_top": "((-1.0, -0.5),(0.0, 0.2))",
                        "peak_range_bottom": "((-0.9, -0.75),(0.0, 0.125))",
                        "method": "Max"
                    },
                    "output": {
                        "file1": "/outputs/version_0415_180633/CV_results.csv",
                        "img1":  "/static/imgs/Picture1.png"
                    },
                    "display": "none"
                },
                "form3": {
                    "status": 'processing',
                    "display": "none"
                },
                "processing_display": "none"
            }
        }
    
    def read_csv(self):
        files = os.listdir(self.filepath)
        files = sorted(files, key=reorder)
        files = filter_files(files)
        if not check_files(files):
            return None

        data = {}
        for f in files:
            if f.endswith(".csv"):
                # input your file name here and switch rpm in to %d
                file = os.path.join(self.filepath, f)
                if not os.path.isfile(file):
                    continue
                print(f)
                rpm = extract_mvs(f)
                if rpm is None:
                    continue
                print(rpm)
                df = pd.read_csv(file, delimiter=',', dtype={'Current range': str})
                data[rpm] = df
        print("data: ", len(data))
        return data
    """

    def read_data(self):
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
        print("len of files: ", len(files), self.files_info)

        data = {}
        for f in files:
            file = real_file_path[f]
            if not os.path.isfile(file):
                continue

            print(f)
            rpm = extract_mvs(f)
            if rpm is None:
                continue
            print(rpm)

            if file.endswith(".xlsx"):
                csv_file = file + ".csv"
                if os.path.exists(csv_file):
                    data[rpm] = pd.read_csv(csv_file, delimiter=',', dtype={'Current range': str})
                else:
                    data0 = pd.ExcelFile(file)
                    data[rpm] = data0.parse('Sheet1')
                    data[rpm].to_csv(csv_file, sep=',', index=False)
                    print("saved csv file to {}".format(csv_file))
            elif file.endswith(".txt"):
                data[rpm] = pd.read_csv(file, delimiter=';', dtype={'Current range': str})
            elif file.endswith(".csv"):
                data[rpm] = pd.read_csv(file, delimiter=',', dtype={'Current range': str})

        print("data: ", len(data))
        return data

    def start1_figure(self, data, apply_sigma=False, sigma=10):
        for scan_rate, df0 in data.items():
            # data0 = pd.ExcelFile(file)
            # df0 = data0.parse('Sheet1')
            df = df0[df0['Scan'] == 6]
            E = df['WE(1).Potential (V)']
            I = df['WE(1).Current (A)']

            # Define the standard deviation (sigma) for the Gaussian filter

            upperE, lowerE, upperI, lowerI = separater(E, I, min(E), max(E))
            if apply_sigma:
                # Apply gaussian_filter with sigma=?
                smoothed_upperI = gaussian_filter(upperI, sigma=sigma)
                smoothed_lowerI = gaussian_filter(lowerI, sigma=sigma)
            else:
                smoothed_upperI = upperI
                smoothed_lowerI = lowerI

            I = np.concatenate((smoothed_upperI, smoothed_lowerI))
            E = upperE + lowerE

            #         print("length of E:",len(E))
            plt.scatter(E, I, label=scan_rate + 'mV', s=1)

        plt.xlabel('Applied potential/V')
        plt.ylabel('Current/A')
        # plt.ylim(-2e-5,2e-5)
        plt.legend()
        # plt.grid()
        # plt.show()

        if apply_sigma:
            to_file1 = os.path.join(self.savepath, "form1_sigma{}.png".format(sigma))
        else:
            to_file1 = os.path.join(self.savepath, "form1_original.png")
        plt.savefig(to_file1)
        plt.close()
        return to_file1

    def start1(self, sigma = 10):
        """
        input: form1
        :return:
        """
        data = self.read_data()
        if data is None:
            return {
                'status': False,
                'message': 'One or more files are not allowed.'
            }

        to_file1 = self.start1_figure(data, apply_sigma=False, sigma=sigma)
        to_file2 = self.start1_figure(data, apply_sigma=True, sigma=sigma)

        data_file = os.path.join('outputs', self.version, 'data.json')
        if os.path.exists(data_file):
            data = json.loads(open(data_file, 'r').read())
        else:
            data = {'version': self.version}

        if 'CV' not in data.keys():
            data['CV'] = {}

        data['CV']['form1'] = {
            'status': 'done',
            'input': {
                'uploaded_files': [],
                'sigma': sigma
            },
            'output': {
                'file1': to_file1 if to_file1.startswith("/") else '/' + to_file1,
                'file2': to_file2 if to_file1.startswith("/") else '/' + to_file2,
            }
        }
        with open(data_file, 'w') as f:
            f.write(json.dumps(data))
            print("saved to: {}".format(data_file))

        return {
            'status': True,
            'version': self.version,
            'message': 'Success',
            'data': data
        }

    def start2_prepare(self, data, method, p1_start, p1_end, p2_start, p2_end):
        Ef1 = []
        DelE01 = []
        Ea1 = []
        Ec1 = []
        Ia1 = []
        Ic1 = []
        Scan_Rate1 = []
        for jj, df0 in data.items():
            j = int(jj.replace("mVs", ""))
            name = str(j) + "mV"
            num = j

            Ea1j = []
            Ec1j = []
            Ia1j = []
            Ic1j = []
            for i in range(3, 12):
                df = df0[df0['Scan'] == i]
                Ui = df['WE(1).Potential (V)']
                Ii = df['WE(1).Current (A)']
                cycle = str(i + 1)
                Ui = np.array(Ui)
                Ii = np.array(Ii)

                upperU, lowerU, upperI, lowerI = separater(Ui, Ii, min(Ui), max(Ui))

                # Apply Gaussian filter(optional)
                apply_gaussian_filter = False  # Set to True to apply the filter, False to not apply the filter

                if apply_gaussian_filter == True:
                    # Apply gaussian_filter with sigma=1
                    smoothed_upperI = gaussian_filter(upperI, sigma=1)
                    smoothed_lowerI = gaussian_filter(lowerI, sigma=1)
                else:
                    # If not applying the filter, assign the original arrays to the new variables
                    smoothed_upperI = upperI
                    smoothed_lowerI = lowerI

                top_x1, top_y1 = find_max(upperU, smoothed_upperI, p1_start, p1_end)
                bottom_x1, bottom_y1 = find_min(lowerU, smoothed_lowerI, p2_start, p2_end)
                DelE01i = top_x1 - bottom_x1
                Ef1i = (top_x1 + bottom_x1) / 2

                Ea1.append(top_x1)
                Ea1j.append(top_x1)
                Ia1.append(find_y(upperU, smoothed_upperI, top_x1))
                Ia1j.append(find_y(upperU, smoothed_upperI, top_x1))
                Ec1.append(bottom_x1)
                Ec1j.append(bottom_x1)
                Ic1.append(find_y(lowerU, smoothed_lowerI, bottom_x1))
                Ic1j.append(find_y(lowerU, smoothed_lowerI, bottom_x1))

                DelE01.append(DelE01i)
                Ef1.append(Ef1i)

                Scan_Rate1.append(num)
                #         print('bottom_x1:',bottom_x1)
                #         print('bottom_y1:',bottom_y1)
            #     plt.scatter(upperU, smoothed_upperI, s=2, c='#1f77b4')
            #     plt.scatter(lowerU, smoothed_lowerI, s=2, c='#ff7f0e')
            #
            # plt.scatter(Ea1j, Ia1j, s=10, c='r')
            # plt.scatter(Ec1j, Ic1j, s=10, c='r')
            # plt.xlabel('Applied potential/V')
            # plt.ylabel('Current/A')
            # # plt.ylim(-2e-5,2e-5)
            # plt.title(name)
            # plt.grid()
            # plt.show()

        return (Ea1, Ia1, Ec1, Ic1, DelE01, Scan_Rate1)

    def start2_figure1(self, data, Ea_res, sigma=10, pr1=None, pr2=None):
        df0 = None
        for k, d in data.items():
            df0 = d
            break

        img_path = os.path.join(self.datapath, "CV_form2_p1.png")
        df = df0[df0['Scan'] == 6]
        Ui = df['WE(1).Potential (V)']
        Ii = df['WE(1).Current (A)']
        Ui = np.array(Ui)
        Ii = np.array(Ii)
        upperU, lowerU, upperI, lowerI = separater(Ui, Ii, min(Ui), max(Ui))

        # Apply Gaussian filter(optional)
        apply_gaussian_filter = True  # Set to True to apply the filter, False to not apply the filter

        if apply_gaussian_filter == True:
            # Apply gaussian_filter with sigma
            smoothed_upperI = gaussian_filter(upperI, sigma=sigma)
            smoothed_lowerI = gaussian_filter(lowerI, sigma=sigma)
        else:
            # If not applying the filter, assign the original arrays to the new variables
            smoothed_upperI = upperI
            smoothed_lowerI = lowerI

        plt.scatter(upperU, smoothed_upperI, s=1, c='#1f77b4')
        plt.scatter(lowerU, smoothed_lowerI, s=1, c='#ff7f0e')
        for pp, (Ea1, Ia1, Ec1, Ic1, DelE01, Scan_Rate1) in enumerate(Ea_res):
            top_x1, top_y1 = find_max(upperU, smoothed_upperI, -1, -0.5)
            bottom_x1, bottom_y1 = find_min(lowerU, smoothed_lowerI, -0.9, -0.75)
            p1_start = pr1[pp][0]
            p1_end = pr1[pp][1]
            p2_start = pr2[pp][0]
            p2_end = pr2[pp][1]

            top_x1, top_y1 = find_max(upperU, smoothed_upperI, p1_start, p1_end)
            bottom_x1, bottom_y1 = find_min(lowerU, smoothed_lowerI, p2_start, p2_end)
            plt.scatter(top_x1, top_y1, s=10, c='r')
            plt.scatter(bottom_x1, bottom_y1, s=10, c='r')

        plt.xlabel('Applied potential/V')
        plt.ylabel('Current/A')
        # plt.ylim(-2e-5,2e-5)
        # plt.grid()
        # plt.show()
        plt.savefig(img_path)
        plt.close()
        return img_path

    def start2_figure2(self, data, Ea_res, sigma=10, pr1=None, pr2=None):
        img_path = os.path.join(self.datapath, "CV_form2_p2.png")

        for jj, df0 in data.items():
            j = int(jj.replace("mVs", ""))
            scan_rate = str(j) + "mV"

            df = df0
            E = df['WE(1).Potential (V)']
            I = df['WE(1).Current (A)']

            # Define the standard deviation (sigma) for the Gaussian filter
            sigma = 10.0  # You can adjust this as needed
            upperE, lowerE, upperI, lowerI = separater(E, I, min(E), max(E))

            # Apply gaussian_filter with sigma=?
            smoothed_upperI = gaussian_filter(upperI, sigma=sigma)
            smoothed_lowerI = gaussian_filter(lowerI, sigma=sigma)

            I = np.concatenate((smoothed_upperI, smoothed_lowerI))
            E = upperE + lowerE

            #         print("length of E:",len(E))
            plt.scatter(E, I, label=scan_rate + 'mV', s=1)

        for pp, (Ea1, Ia1, Ec1, Ic1, DelE01, Scan_Rate1) in enumerate(Ea_res):
            # print("===", pp, Ea1, Ia1, Ec1, Ic1)
            plt.scatter(Ea1, Ia1, s=10, c='r')
            plt.scatter(Ec1, Ic1, s=10, c='r')

        plt.xlabel('Applied potential/V')
        plt.ylabel('Current/A')
        # plt.ylim(-2e-5,2e-5)
        # plt.grid()
        # plt.show()
        plt.legend()
        plt.savefig(img_path)
        plt.close()
        return img_path

    def start2(self, method, peak_range_top, peak_range_bottom):

        Ef1 = []
        DelE01 = []
        sigma = self.res_data['CV']['form1']['input']['sigma']

        pr1 = extract_peak_range(peak_range_top)
        pr2 = extract_peak_range(peak_range_bottom)
        for i in range(len(pr1)):
            Ef1.append({})
            DelE01.append({})


        Ea_res = []
        data = self.read_data()
        for pp, pr in enumerate(pr1):
            p1_start = pr1[pp][0]
            p1_end = pr1[pp][1]
            p2_start = pr2[pp][0]
            p2_end = pr2[pp][1]
            print("p1_start, p1_end:", p1_start, p1_end)
            print("p2_start, p2_end:", p2_start, p2_end)

            res = self.start2_prepare(data, method, p1_start, p1_end, p2_start, p2_end)
            Ea_res.append(res)

            for jj, df0 in data.items():
                j = int(jj.replace("mVs", ""))
                name = str(j) + "mV"
                num = j

                Ea1j = []
                Ec1j = []
                Ia1j = []
                Ic1j = []
                for i in range(3, 12):
                    # for i in range(2,3):
                    df = df0[df0['Scan'] == i]
                    Ui = df['WE(1).Potential (V)']
                    Ii = df['WE(1).Current (A)']
                    cycle = str(i + 1)
                    Ui = np.array(Ui)
                    Ii = np.array(Ii)

                    # separate top and bottom

                    upperU, lowerU, upperI, lowerI = separater(Ui, Ii, min(Ui), max(Ui))

                    # Apply Gaussian filter(optional)
                    apply_gaussian_filter = False  # Set to True to apply the filter, False to not apply the filter

                    if apply_gaussian_filter == True:
                        # Apply gaussian_filter with sigma=1
                        smoothed_upperI = gaussian_filter(upperI, sigma=sigma)
                        smoothed_lowerI = gaussian_filter(lowerI, sigma=sigma)
                    else:
                        # If not applying the filter, assign the original arrays to the new variables
                        smoothed_upperI = upperI
                        smoothed_lowerI = lowerI

                    # input range of first peak

                    top_x1, top_y1 = find_max(upperU, smoothed_upperI, p1_start, p1_end)
                    bottom_x1, bottom_y1 = find_min(lowerU, smoothed_lowerI, p2_start, p2_end)
                    DelE01i = top_x1 - bottom_x1
                    Ef1i = (top_x1 + bottom_x1) / 2

                    # Ea1[pp].append(top_x1)
                    Ea1j.append(top_x1)
                    # Ia1[pp].append(find_y(upperU, smoothed_upperI, top_x1))
                    Ia1j.append(find_y(upperU, smoothed_upperI, top_x1))
                    # Ec1[pp].append(bottom_x1)
                    Ec1j.append(bottom_x1)
                    # Ic1[pp].append(find_y(lowerU, smoothed_lowerI, bottom_x1))
                    Ic1j.append(find_y(lowerU, smoothed_lowerI, bottom_x1))

                    if num not in DelE01[pp].keys():
                        DelE01[pp][num] = []
                        Ef1[pp][num] = []

                    DelE01[pp][num].append(DelE01i)
                    Ef1[pp][num].append(Ef1i)

                    # Scan_Rate1[pp].append(num)
                    #         print('bottom_x1:',bottom_x1)
                    #         print('bottom_y1:',bottom_y1)
                #     plt.scatter(upperU, smoothed_upperI, s=2, c='#1f77b4')
                #     plt.scatter(lowerU, smoothed_lowerI, s=2, c='#ff7f0e')
                #
                # plt.scatter(Ea1j, Ia1j, s=10, c='r')
                # plt.scatter(Ec1j, Ic1j, s=10, c='r')
                # plt.xlabel('Applied potential/V')
                # plt.ylabel('Current/A')
                # # plt.ylim(-2e-5,2e-5)
                # plt.title(name)
                # plt.grid()
                # plt.show()

        # Figure 1 and Figure 2:
        img1 = self.start2_figure1(data, Ea_res, sigma, pr1, pr2)
        img2 = self.start2_figure2(data, Ea_res, sigma, pr1, pr2)

        to_data = []
        for pp in range(len(pr1)):
            for mvs in Ef1[pp].keys():
                item = {
                    'peak_range_top': "({},{})".format(pr1[pp][0], pr1[pp][1]),
                    'peak_range_bottom': "({},{})".format(pr2[pp][0], pr2[pp][1]),
                    'mVs': mvs,
                    'fp': np.mean(Ef1[pp][mvs]),
                    'ps': np.mean(DelE01[pp][mvs]),
                }
                to_data.append(item)
        df = pd.DataFrame(to_data)
        to_file = "{}/CV_results.csv".format(self.savepath)
        df.to_csv(to_file, index=False, sep=",")
        print("saved to {}".format(to_file))

        data = self.res_data

        if 'CV' not in data.keys():
            data['CV'] = {}

        data['CV']['form2'] = {
            'status': 'done',
            'input': {
                'peak_range_top': "({},{})".format(pr1[0], pr1[1]),
                'peak_range_bottom': "({},{})".format(pr2[0], pr2[1]),
                'method': method
            },
            'output': {
                'file1': to_file if to_file.startswith("/") else '/' + to_file,
                'img1': img1 if img1.startswith("/") else '/' + img1,
                'img2': img2 if img2.startswith("/") else '/' + img2,
            }
        }
        self.save_result_data(data)

        return {
            'status': True,
            'version': self.version,
            'message': 'Success',
            'data': data
        }


if __name__ == '__main__':
    c = CV("version_test_CV", "data/CV_csv", sigma=10.0)
    # print(c.start1())
    res = c.start2(method='Max', peak_range_top='(-1,-0.5),(0,0.2),(0.25,0.5)',
                   peak_range_bottom='(-0.9,-0.75),(0,0.125),(0.125,0.25)')
    print(res)
