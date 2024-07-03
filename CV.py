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
import ast

colors = [
    '#1f77b4',  # tab:blue
    '#ff7f0e',  # tab:orange
    '#2ca02c',  # tab:green
    '#d62728',  # tab:red
    '#9467bd',  # tab:purple
    '#8c564b',  # tab:brown
    '#e377c2',  # tab:pink
    '#7f7f7f',  # tab:gray
    '#bcbd22',  # tab:olive
    '#17becf'   # tab:cyan
]


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


def Search_scan_rate(filename):
    match = re.search(r'(\d+)mVs', filename)
    if match:
        return int(match.group(1))
    else:
        # Handle files without RPM values
        return -1  # You can use any default value or treatment


def Milad(filename):
    match = re.search(r'PFOS_(\d+)', filename)
    if match:
        return int(match.group(1))
    else:
        # Handle files without RPM values
        return -1  # You can use any default value or treatment


def read_ec_lab_file(file_path, encoding='utf-8'):
    with open(file_path, 'r', encoding=encoding) as file:
        lines = file.readlines()

    # Determine the number of header lines
    num_header_lines = 56  # As per the given pattern

    # Extract the data lines (skipping the header)
    data_lines = lines[num_header_lines:]

    # Create a list to store the extracted data
    data = []

    for line in data_lines:
        if line.strip():  # Ignore empty lines
            parts = line.split()
            if len(parts) == 2:
                ewe, i_mA = parts
                data.append((float(ewe), float(i_mA)))

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['Ewe/V', '<I>/mA'])
    return df


def read_auto_lab_file(file):
    if file.endswith('.csv'):
        df = pd.read_csv(file, delimiter=',')
    else:
        df = pd.read_excel(file, sheet_name='Sheet1', engine='openpyxl')
    return df


def create_file_template_CV(file_name):
    # Use a regular expression to find the rpm part
    pattern = r'(\d+)mVs'

    # Replace the numeric rpm part with a placeholder for formatting later
    template = re.sub(pattern, '%dmVs', file_name)

    return template


def make_color_darker(color, factor):
    # Extract the RGB components from the hex color string
    r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)

    # Apply the darkening factor to each component
    r = max(0, int(r * factor))
    g = max(0, int(g * factor))
    b = max(0, int(b * factor))

    # Convert the darkened RGB values back to a hex color string
    return f'#{r:02x}{g:02x}{b:02x}'

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

    def start1_figure(self, data, apply_sigma=False, all_params = {}):
        cycle = int( all_params['cycle'] )
        sigma = float( all_params['sigma'] )

        # WIth cycle
        for scan_rate, df0 in data.items():
            # data0 = pd.ExcelFile(file)
            # df0 = data0.parse('Sheet1')
            df = df0[df0['Scan'] == cycle]
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

        # No cycle
        for scan_rate, df0 in data.items():
            # data0 = pd.ExcelFile(file)
            # df0 = data0.parse('Sheet1')
            df = df0
            E = df['WE(1).Potential (V)']
            I = df['WE(1).Current (A)']
            plt.scatter(E, I, label=scan_rate + 'mV', s=1)
        plt.xlabel('Applied potential/V')
        plt.ylabel('Current/A')
        plt.legend()
        to_file3 = os.path.join(self.savepath, "form1_cycle.png")
        plt.savefig(to_file3)
        plt.close()
        return to_file1, to_file3

    def start1(self, all_params):
        """
        input: form1
        :return:
        """
        sigma = float(all_params['sigma'])

        data = self.read_data()
        if data is None:
            return {
                'status': False,
                'message': 'One or more files are not allowed.'
            }

        to_file1, to_file3 = self.start1_figure(data, apply_sigma=False, all_params=all_params)
        to_file2, _ = self.start1_figure(data, apply_sigma=True, all_params=all_params)

        data_file = os.path.join('outputs', self.version, 'data.json')
        if os.path.exists(data_file):
            data = json.loads(open(data_file, 'r').read())
        else:
            data = {'version': self.version}

        if 'CV' not in data.keys():
            data['CV'] = {}

        all_params['uploaded_files'] = []
        data['CV']['form1'] = {
            'status': 'done',
            'input': all_params,
            'output': {
                'file1': to_file1 if to_file1.startswith("/") else '/' + to_file1,
                'file2': to_file2 if to_file2.startswith("/") else '/' + to_file2,
                'file3': to_file3 if to_file3.startswith("/") else '/' + to_file3,
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

        return (Ef1, DelE01, Ea1, Ec1, Ia1, Ic1, Ic1, Scan_Rate1)

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
            # Apply gauplt.savefig(img_path)ssian_filter with sigma
            smoothed_upperI = gaussian_filter(upperI, sigma=sigma)
            smoothed_lowerI = gaussian_filter(lowerI, sigma=sigma)
        else:
            # If not applying the filter, assign the original arrays to the new variables
            smoothed_upperI = upperI
            smoothed_lowerI = lowerI

        plt.scatter(upperU, smoothed_upperI, s=1, c='#1f77b4')
        plt.scatter(lowerU, smoothed_lowerI, s=1, c='#ff7f0e')
        for pp, (Ef1, DelE01, Ea1, Ec1, Ia1, Ic1, Ic1, Scan_Rate1) in enumerate(Ea_res):
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

        for pp, (Ef1, DelE01, Ea1, Ec1, Ia1, Ic1, Ic1, Scan_Rate1) in enumerate(Ea_res):
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

    def start2(self, all_params):
        print(all_params)


        method = all_params['method']
        # peak_range_top = all_params['peak_range_top']
        # peak_range_bottom = all_params['peak_range_bottom']

        peak_info = {}
        peak_range_ox = ast.literal_eval(all_params['peak_range_top']) # [(-1, -0.70), (0, 0.2), (0.25, 0.5)]
        peak_range_re = ast.literal_eval(all_params['peak_range_bottom'])  #[(-0.925, -0.75), (0.0, 0.125), (0.125, 0.25)]
        discard_scan = [0, 0, 2]
        example_scan_rate = all_params['scan_rate'] # default 20
        example_cycle  = all_params['cycle'] # default 9

        sigma = float(self.res_data['CV']['form1']['input']['sigma'])

        # read data
        with open(self.files_info, 'r') as f:
            info_list = json.loads(f.read())
        files = []
        real_file_path = {}
        for info in info_list:
            # input your file name here and switch rpm in to %d
            f = info['filename']
            ef = info['existed_filename']
            if not os.path.isfile(ef):
                continue
            files.append(f)
            real_file_path[f] = ef
        files = sorted(files, key=Search_scan_rate)
        device = f'Autolab'
        if device == 'Autolab':
            Filter_files = [file for file in files if file.endswith('.xlsx') or file.endswith('.csv')]
        elif device == 'EClab':
            Filter_files = [file for file in files if file.endswith('.txt')]
        else:
            Filter_files = []
            print('device not found in library')
        file_template = os.path.splitext(create_file_template_CV(Filter_files[0]))[0]
        data_list = []
        for file in Filter_files:
            scan_rate = Search_scan_rate(file)
            df = read_auto_lab_file(real_file_path[file])
            var_name = file_template % scan_rate
            globals()[var_name] = df
            data_list.append(var_name)
            print(var_name)



        cycle_range = range(2, 15)

        for z in range(len(peak_range_ox)):
            peak_info[f'Ef{z}'] = []
            peak_info[f'DelE0{z}'] = []
            peak_info[f'Ea{z}'] = []
            peak_info[f'Ec{z}'] = []
            peak_info[f'Ia{z}'] = []
            peak_info[f'Ic{z}'] = []
            peak_info[f'Scan_Rate{z}'] = []

            # Create a new figure for each z loop
            print(f'\n\033[1mFigure Set for Peak{z + 1}:\033[0m')
            plt.figure()

            # Determine the slice based on the variable
            if discard_scan[z] == 0:
                selected_data_list = data_list
            else:
                selected_data_list = data_list[:-discard_scan[z]]
                print(f'Last {discard_scan[z]} scans were discarded for Peak {z + 1}')

            # Find peak position
            for var_name in selected_data_list:
                df = globals()[var_name]
                print(var_name)
                scan_rate = Search_scan_rate(var_name)
                name = str(scan_rate) + "mV"

                # Initialize lists for this file
                Ea_j = []
                Ec_j = []
                Ia_j = []
                Ic_j = []

                for i in cycle_range:
                    cycle_df = df[df['Scan'] == i]
                    if len(cycle_df) == 0:
                        continue
                    Ui = cycle_df['WE(1).Potential (V)']
                    Ii = cycle_df['WE(1).Current (A)']
                    Ui = np.array(Ui)
                    Ii = np.array(Ii)

                    # Separate top and bottom
                    upperU, lowerU, upperI, lowerI = separater(Ui, Ii, min(Ui), max(Ui))


                    # Apply Gaussian filter (optional)
                    apply_gaussian_filter = False  # Set to True to apply the filter, False to not apply the filter

                    if apply_gaussian_filter:
                        smoothed_upperI = gaussian_filter(upperI, sigma=1)
                        smoothed_lowerI = gaussian_filter(lowerI, sigma=1)
                    else:
                        smoothed_upperI = upperI
                        smoothed_lowerI = lowerI

                    # Input range of first peak
                    top_x, top_y = find_max(upperU, smoothed_upperI, peak_range_ox[z][0], peak_range_ox[z][1])
                    bottom_x, bottom_y = find_min(lowerU, smoothed_lowerI, peak_range_re[z][0], peak_range_re[z][1])
                    DelE02i = top_x - bottom_x
                    Ef2i = (top_x + bottom_x) / 2

                    peak_info[f'Ea{z}'].append(top_x)
                    Ea_j.append(top_x)
                    peak_info[f'Ia{z}'].append(find_y(upperU, smoothed_upperI, top_x))
                    Ia_j.append(find_y(upperU, smoothed_upperI, top_x))
                    peak_info[f'Ec{z}'].append(bottom_x)
                    Ec_j.append(bottom_x)
                    peak_info[f'Ic{z}'].append(find_y(lowerU, smoothed_lowerI, bottom_x))
                    Ic_j.append(find_y(lowerU, smoothed_lowerI, bottom_x))

                    peak_info[f'DelE0{z}'].append(DelE02i)
                    peak_info[f'Ef{z}'].append(Ef2i)

                    peak_info[f'Scan_Rate{z}'].append(scan_rate)

        # Dictionary to store the mean values of Ef
        mean_Ef = {}

        for i in range(len(discard_scan)):
            Ef = np.mean(peak_info[f'Ef{i}'])
            mean_Ef[f'Ef{i + 1}'] = Ef

        ## show all searched peaks on the CV plot figure
        plt.figure()
        # Plot the CV data
        for data_i in data_list:
            df = globals()[data_i]  # Access the DataFrame using the variable name
            print(data_i)
            U = df['WE(1).Potential (V)']
            I = df['WE(1).Current (A)']
            scan_rate = Search_scan_rate(data_i)  # Extract scan rate from the variable name
            plt.scatter(U, I, label=f'{scan_rate} mV', s=1, c='#1f77b4')

        # Plot the peak information
        for i in range(len(peak_range_ox)):
            plt_data_Ea = peak_info[f'Ea{i}']
            plt_data_Ec = peak_info[f'Ec{i}']
            plt_data_Ia = peak_info[f'Ia{i}']
            plt_data_Ic = peak_info[f'Ic{i}']
            plt.scatter(plt_data_Ea, plt_data_Ia, s=10, c='r')
            plt.scatter(plt_data_Ec, plt_data_Ic, s=10, c='r')

        plt.xlabel('Applied potential/V')
        plt.ylabel('Current/A')
        plt.legend()
        # plt.show()
        to_file1 = os.path.join(self.datapath, "CV_step2_p1.png")
        plt.savefig(to_file1)
        plt.close()


        search_key = str(example_scan_rate) + "mV"
        # Find all names containing "10mVs"
        matching_data = [name for name in data_list if search_key in name]
        print(matching_data)
        df = globals()[matching_data[0]]
        df = df[df['Scan'] == int(example_cycle)]
        U = df['WE(1).Potential (V)']
        I = df['WE(1).Current (A)']

        plt.figure()

        # Separate top and bottom
        upperU, lowerU, upperI, lowerI = separater(U, I, min(U), max(U))

        if apply_gaussian_filter:
            smoothed_upperI = gaussian_filter(upperI, sigma=1)
            smoothed_lowerI = gaussian_filter(lowerI, sigma=1)
        else:
            smoothed_upperI = upperI
            smoothed_lowerI = lowerI

        plt.scatter(upperU, smoothed_upperI, s=1, c='#1f77b4')
        plt.scatter(lowerU, smoothed_lowerI, s=1, c='#ff7f0e')

        for z in range(len(peak_range_ox)):
            top_x, top_y = find_max(upperU, smoothed_upperI, peak_range_ox[z][0], peak_range_ox[z][1])
            bottom_x, bottom_y = find_min(lowerU, smoothed_lowerI, peak_range_re[z][0], peak_range_re[z][1])
            plt.scatter(top_x, top_y, s=20, c='r')
            plt.scatter(bottom_x, bottom_y, s=20, c='r')
        plt.xlabel('Applied potential/V')
        plt.ylabel('Current/A')
        # plt.show()
        to_file2 = os.path.join(self.datapath, "CV_step2_p2.png")
        plt.savefig(to_file2)
        plt.close()


        # Save tmp results
        tmp_res_filename = "form2_res.pkl"
        # tmp_res = {
        #     'Ea_res': Ea_res,
        #     'pr1': pr1,
        #     'pr2': pr2,
        # }
        # self.pkl_save(tmp_res, tmp_res_filename)


        data = self.res_data

        if 'CV' not in data.keys():
            data['CV'] = {}

        data['CV']['form2'] = {
            'status': 'done',
            'input': all_params,
            'output': {
                # 'file1': to_file if to_file.startswith("/") else '/' + to_file,
                'img1': to_file1 if to_file1.startswith("/") else '/' + to_file1,
                'img2': to_file2 if to_file2.startswith("/") else '/' + to_file2,
            }
        }
        self.save_result_data(data)

        return {
            'status': True,
            'version': self.version,
            'message': 'Success',
            'data': data
        }


    def start4(self, n, a):
        form2_res = self.pkl_load("form2_res.pkl")

        F = 96485.3321  # Faraday's constant in C/mol
        R = 8.3145  # Gas constant in J/(mol*K)

        # input value
        # a = 0.5
        # n = 1

        Ea_res = form2_res['Ea_res']

        DD = [2.5e-6, 3.5e-5, 3e-4]

        res = []
        for pp, (Ef1, DelE01, Ea1, Ec1, Ia1, Ic1, Ic1, Scan_Rate1) in enumerate(Ea_res):

            try:
                D1 = DD[pp]
            except Exception as e:
                D1 = 2.5e-6

            DelE01 = DelE01[:36]
            Scan_Rate1 = Scan_Rate1[:36]

            DelE01_mV = np.array(DelE01) * 1000
            print(DelE01_mV)
            T = 298.15  # 25 degrees Celsius in Kelvin
            fai = [2.18 * ((a / math.pi) ** 0.5) * math.exp(-((a ** 2 * F) / (R * T)) * n * DelE) for DelE in DelE01]

            plt.scatter(DelE01_mV, fai, s=5)
            plt.xlabel('$\Delta E_p$ (mV)')
            plt.ylabel('$\Psi$')
            img_path1 = os.path.join(self.datapath, "CV_form4_interval{}_p1.png".format(pp))
            plt.savefig(img_path1)
            # plt.grid()
            # plt.show()
            plt.close()

            # Calculate the term [πDnF/RT]-1/2
            term = ((math.pi * D1 * n * F) / (R * T)) ** (-1 / 2)

            # Calculate x-axis values
            Scan_Rate_V = [rate / 1000 for rate in Scan_Rate1]
            x_axis = [term * (vi ** (-1 / 2)) for vi in Scan_Rate_V]

            # Plot fai against the term multiplied by v^(-1/2)
            plt.scatter(x_axis, fai, s=1)
            plt.xlabel('$[πDnνF/RT]^{-1/2}$' + str(term) + '$v^{-1/2}$')
            plt.ylabel('$\Psi$')
            # plt.grid()

            # Perform linear regression
            slope, intercept = np.polyfit(x_axis, fai, 1)

            # Add linear regression line to the plot
            plt.plot(x_axis, slope * np.array(x_axis) + intercept, color='red')
            # Display the equation of the linear regression line on the plot
            equation = f"$y = {slope:.4f}x + {intercept:.4f}$"
            plt.text(0.1, 0.9, equation, transform=plt.gca().transAxes)

            # Display the slope
            print("Slope:", slope)

            # plt.show()
            img_path2 = os.path.join(self.datapath, "CV_form4_interval{}_p2.png".format(pp))
            plt.savefig(img_path2)
            plt.close()

            res.append({
                'img1': img_path1 if img_path1.startswith("/") else '/' + img_path1,
                'img2': img_path2 if img_path2.startswith("/") else '/' + img_path2,
                'slope': slope,
            })

        data = self.res_data

        if 'CV' not in data.keys():
            data['CV'] = {}

        data['CV']['form4'] = {
            'status': 'done',
            'input': {
                'n': n,
                'a': a,
            },
            'output': {
                'files': res
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
