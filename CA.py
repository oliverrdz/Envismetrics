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
        pass

if __name__ == '__main__':
    c = CA("version_test_CV")


