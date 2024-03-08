import re
import numpy as np
import pandas as pd
import os as os
import matplotlib
import matplotlib.pyplot as plt
import math
from sklearn.linear_model import LinearRegression
from scipy.ndimage import gaussian_filter
matplotlib.use('Agg')

# Function to find y value (I) corresponding to given x value (potential)
# It finds the index of the element in the array x that is closest to the target_x value using
def find_y(x, y, target_x):
    index = np.argmin(np.abs(x - target_x))
    return y[index]

def find_y_exact(x,y,target_x):
    index = np.where(x == target_x)[0]
    return y[index]

def rpm_to_rads(rpm):
    rps = rpm / 60  # Convert RPM to RPS (revolutions per second)
    rad_per_sec = 2 * math.pi * rps  # Convert RPS to rad/s
    return rad_per_sec

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

class HDV(object):
    def __init__(self, version, filepath):
        self.version = version
        self.filepath = filepath
        self.savepath = 'outputs'

    def read_data(self, files):
        data = {}
        for f in files:
            # input your file name here and switch rpm in to %d
            file = os.path.join(self.filepath, f)
            if not os.path.isfile(file):
                continue
            print(f)
            rpm = extract_rpm(f)
            if rpm is None:
                continue
            print(rpm)
            if f.endswith(".xlsx"):
                data0 = pd.ExcelFile(file)
                data[rpm] = data0.parse('Sheet1')
            elif f.endswith(".txt"):
                df = pd.read_csv(file, delimiter=';')
                data[rpm] = df
        print("data: ", len(data))
        return data

    def start(self):
        files = os.listdir(self.filepath)
        files = sorted(files, key=reorder)
        if not check_files(files):
            return {
                'status': False,
                'message': 'One or more files are not allowed.'
            }

        data = self.read_data(files)

        for rpm, df in data.items():
            E = df['WE(1).Potential (V)']
            I = df['WE(1).Current (A)']
            print("length of E:", len(E))
            plt.scatter(E, I, label=rpm, s=1)
        plt.xlabel('Applied potential/V')
        plt.ylabel('Current/A')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
        #plt.xlim()
        # plt.ylim(-0.0002,0.0003)
        plt.legend()
        plt.grid()
        # plt.show()
        to_file1 = os.path.join(self.savepath, "{}_1.png".format(self.version))
        plt.savefig(to_file1)
        plt.close()

        # plot figure modlue with Gaussian filter

        # Create an empty DataFrame to store the data
        combined_data = pd.DataFrame()

        for rpm, df in data.items():
            E = df['Potential applied (V)']
            I = df['WE(1).Current (A)']
            # Define the standard deviation (sigma) for the Gaussian filter
            sigma = 10.0  # You can adjust this as needed
            # Apply the Gaussian filter to the 'Current (A)'
            smoothed_I = gaussian_filter(I, sigma=sigma)
            print("length of E:", len(E))
            plt.scatter(E, smoothed_I, label=rpm, s=1)

            # Create a new DataFrame for the current RPM
            rpm_data = pd.DataFrame({'Potential (V)' + rpm: E, 'Current (A)' + rpm: I})
            # Concatenate the data for this RPM to the right of the combined_data DataFrame
            combined_data = pd.concat([combined_data, rpm_data], axis=1)

        plt.xlabel('Applied potential/V')
        plt.ylabel('Current/A')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        # plt.xlim(-1.0,0.5)
        # plt.ylim(-0.00006, 0.00008)
        plt.legend()
        plt.grid()
        # plt.show()
        to_file2 = os.path.join(self.savepath, "{}_2.png".format(self.version))
        plt.savefig(to_file2)
        plt.close()
        return {
            'status': True,
            'message': 'Success',
            'file1': to_file1,
            'file2': to_file2
        }


if __name__ == '__main__':
    hdv = HDV('', "static/data")
    hdv.start()


