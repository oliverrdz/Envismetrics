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

def get_num(filename):
    # 定义要匹配的字符串
    # filename = "(3)PFOA400ppm_75075_50s_CA.xlsx"
    # filename = "3PFOA400ppm_75075_50s_CA.xlsx"

    # 使用正则表达式匹配数字部分
    match = re.search(r'(\d+)', filename)

    # 如果匹配成功，则打印括号中的内容
    if match:
        result = match.group(1)
        return int(result)
    else:
        return None


class CA(BaseModule):
    def __init__(self, version):
        super().__init__(version)

    def step1(self):
        data = self.read_data()
        for d in data:
            filename = d['filename']
            df = d['df']

            t = df['Time (s)']
            I = df['WE(1).Current (A)']
            U = df['WE(1).Potential (V)']
            plt.plot(t, U, linestyle='-', linewidth=1, color='#1f77b4')

        plt.xlabel('time/s')
        plt.ylabel('Applied potential/V')
        plt.title('A', loc='left', bbox=dict(facecolor='white', edgecolor='black'))
        # plt.ylim(-2e-5,2e-5)
        # plt.grid()
        # plt.show()
        to_file1 = os.path.join(self.datapath, "CA_form1_p1.png")
        plt.savefig(to_file1)
        plt.close()


        for d in data:
            filename = d['filename']
            df = d['df']

            t = df['Time (s)']
            I = df['WE(1).Current (A)']
            U = df['WE(1).Potential (V)']

            plt.scatter(t, I, s=1, c='#1f77b4')

        plt.xlabel('time/s')
        plt.ylabel('Current/A')
        plt.title('B', loc='right', bbox=dict(facecolor='white', edgecolor='black'))
        # plt.ylim(-2e-5,2e-5)
        # plt.grid()
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

        to_file2 = os.path.join(self.datapath, "CA_form1_p2.png")
        plt.savefig(to_file2)
        plt.close()

        data_file = os.path.join(self.datapath, 'data.json')
        if os.path.exists(data_file):
            data = json.loads(open(data_file, 'r').read())
        else:
            data = {'version': self.version}

        if 'CA' not in data.keys():
            data['CA'] = {}

        data['CA']['form1'] = {
            'status': 'done',
            'input': {
                'uploaded_files': [],
                # 'sigma': self.sigma
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


    def step2(self, interval, n, a, c, x_range=''):
        data = self.read_data()

        # n = 1
        F = 96485
        d_electrode = 0.3
        # A = math.pi * ((d_electrode / 2) ** 2)
        A = a
        print('electrode area (cm2):', A)

        # C0 = 0.000966e-3  # in (mol/cm3)
        C0 = c

        range_start, range_end = x_range.replace("[", "").replace("]", "").split(',')
        range_start = float(range_start)
        range_end = float(range_end)

        slope_set = []
        D_set = []
        R2_set = []

        to_files = []

        for d in data:
            filename = d['filename']
            df = d['df']
            j = get_num(filename)

            if j > interval:
                continue

            t = df['Time (s)'] - df['Time (s)'].iloc[0]
            I = df['WE(1).Current (A)']
            U = df['WE(1).Potential (V)']

            t_inverse_05 = t ** (-0.5)
            Bt = ((n * F * A * C0) / (math.pi ** 0.5)) * t_inverse_05

            # Plot t vs I
            plt.scatter(t, I, s=2, color='#1f77b4')
            plt.xlabel('Time (s)')
            plt.ylabel('Current (A)')
            plt.subplots_adjust(left=0.2)  # 将左边距设置为 0.2，单位是相对于图像宽度的比例
            # plt.grid()
            # plt.show()
            to_file1 = os.path.join(self.datapath, "CA_form2_p{}_1.png".format(j))
            plt.savefig(to_file1)
            plt.close()

            Bt = Bt[2:]
            I = I[2:]

            regression_mask = (Bt >= range_start) & (Bt <= range_end)
            Bt = Bt[regression_mask]
            I = I[regression_mask]

            # Perform linear regression Bt vs I
            slope, intercept = np.polyfit(Bt, I, 1)
            D = slope ** 2

            slope_set.append(slope)
            D_set.append(D)

            # Calculate R-squared value
            residuals = I - (slope * Bt + intercept)
            ss_residuals = np.sum(residuals ** 2)
            ss_total = np.sum((I - np.mean(I)) ** 2)
            r_squared = 1 - (ss_residuals / ss_total)

            R2_set.append(r_squared)

            # Plot Bt vs I with the regression line
            plt.scatter(Bt, I, s=2, color='#1f77b4')
            plt.plot(Bt, slope * Bt + intercept, color='red', label='Regression Line')
            plt.xlabel('nFAC₀ π ⁻¹/² t⁻¹/²')

            plt.ylabel('Current (A)')
            # plt.grid()
            plt.legend()
            plt.subplots_adjust(left=0.2)  # 将左边距设置为 0.2，单位是相对于图像宽度的比例
            # plt.show()
            to_file2 = os.path.join(self.datapath, "CA_form2_p{}_2.png".format(j))
            plt.savefig(to_file2)
            plt.close()

            print(j, "Slope:", slope)
            print(j, "R-squared:", r_squared)
            print(j, "D:", D)
            to_files.append( [
                to_file1 if to_file1.startswith("/") else '/' + to_file1,
                to_file2 if to_file2.startswith("/") else '/' + to_file2,
            ])

        table = pd.DataFrame([slope_set, D_set, R2_set], index=['slope', 'D', 'R2'])
        # New column names starting from 'interval2'
        length_of_D_set = len(table.loc['D'])
        new_column_names = ['interval{}'.format(i + 2) for i in range(length_of_D_set)]
        # Assign the new column names to the DataFrame
        table.columns = new_column_names
        to_file_csv = os.path.join(self.datapath, "CA_form2.csv")
        table.to_csv(to_file_csv, index=True, sep=',')
        print("saved to: {}".format(to_file_csv))

        data = self.res_data

        if 'CA' not in data.keys():
            data['CA'] = {}

        data['CA']['form2'] = {
            'status': 'done',
            'input': {
                'uploaded_files': [],
                # 'sigma': self.sigma
            },
            'output': {
                'files': to_files,
                'csv_file': to_file_csv if to_file_csv.startswith("/") else '/' + to_file_csv,
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
    c = CA("version_test_CV")


