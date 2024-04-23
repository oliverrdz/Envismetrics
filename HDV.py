import re
import numpy as np
import pandas as pd
import os as os
import matplotlib
import matplotlib.pyplot as plt
import math
import json
from BaseModule import BaseModule
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

class HDV(BaseModule):
    def __init__(self, version):
        super().__init__(version)


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

        data = {}
        for f in files:
            file = real_file_path[f]
            if not os.path.isfile(file):
                continue
            print(f)
            rpm = extract_rpm(f)
            if rpm is None:
                continue
            print(rpm)
            if file.endswith(".xlsx"):
                csv_file = file + ".csv"
                if os.path.exists(csv_file):
                    data[rpm] = pd.read_csv(csv_file, sep=',')
                else:
                    data0 = pd.ExcelFile(file)
                    data[rpm] = data0.parse('Sheet1')
                    data[rpm].to_csv(csv_file, sep=',', index=False)
                    print("saved csv file to {}".format(csv_file))
            elif file.endswith(".txt"):
                df = pd.read_csv(file, delimiter=';')
                data[rpm] = df
        print("data: ", len(data))
        return data


    def step1(self):
        data = self.read_data()

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
        to_file1 = os.path.join(self.datapath, "step1_p1.png")
        plt.savefig(to_file1)
        plt.close()

        # plot figure modlue with Gaussian filter

        # Create an empty DataFrame to store the data
        combined_data = pd.DataFrame()

        # Define the standard deviation (sigma) for the Gaussian filter
        sigma = 10

        for rpm, df in data.items():
            E = df['Potential applied (V)']
            I = df['WE(1).Current (A)']

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
        to_file2 = os.path.join(self.datapath, "step1_p2.png")
        plt.savefig(to_file2)
        plt.close()

        data = self.res_data
        if 'HDV' not in data.keys():
            data['HDV'] = {}
        data['HDV']['form1'] = {
            'status': 'done',
            'input': {
                'sigma': 10,
            },
            'output': {
                'file1': to_file1 if to_file1.startswith("/") else '/' + to_file1,
                'file2': to_file2 if to_file2.startswith("/") else '/' + to_file2,
                # 'img1': '/outputs/version_test_CV/form2.jpg',
            }
        }
        self.save_result_data(data)

        return {
            'status': True,
            'version': self.version,
            'message': 'Success',
            'data': data
        }

    def _step2_1_fig1(self, data, input_n=1, input_a = 1.0, input_v = 0.01, input_c = 0.000894454e-3 ):
        # Define constants and parameters_These are setting parameter
        start_value = -1.0  # Starting value of the range for potential
        end_value = 0.25  # Ending value of the range for potential
        n_points = 9  # Number of points to select

        # These are calculation parameter
        n = input_n
        relectrode = 0.15  # Radius of the rotate electrode
        print('electrode Radius is :', relectrode, 'cm')
        A = np.pi * (relectrode ** 2)
        print('surface area is :', A, 'cm\u00b2')
        v = input_v  # kinematic viscosity of the solution (ν - cm2/s),
        C = input_c  # in mol/cm3

        # Load data
        Levich_plotshow_data = pd.DataFrame()

        data = self.read_data()
        E = None
        for rpm, df in data.items():
            E = df['WE(1).Potential (V)']
            break

        # Calculate the corresponding indices within the range
        start_index = E[E >= start_value].idxmin()
        end_index = E[E <= end_value].idxmax()
        points_number = np.linspace(start_index, end_index, n_points, dtype=int)
        E_selected = E.iloc[points_number]
        Levich_slope = []
        Levich_intercept = []
        D = []

        try:
            sigma = self.res_data['HDV']['form1']['input']['sigma']
        except Exception as e:
            sigma = 10.0

        for j, potential in enumerate(E_selected):
            # find the corresponding I
            print(f"potential {j + 1} : {potential:.4f} V")
            I_elected = []
            w_05 = []

            for rpm, df in data.items():
                # x axis（w）
                w_i = rpm_to_rads(int(rpm.replace('rpm', '')))
                w05_i = w_i ** 0.5
                w_05.append(w05_i)

                # y axis (Ii)
                E = df['Potential applied (V)']
                I = df['WE(1).Current (A)']
                # Apply the Gaussian filter to the 'Current (A)'
                smoothed_I = gaussian_filter(I, sigma=sigma)

                I_potential_i = find_y(E, smoothed_I, potential)
                # print(I_potential_i)
                I_elected.append(I_potential_i)

            plt.scatter(w_05, I_elected, s=3)

            # Create a new DataFrame for the current RPM

            potential_data = pd.DataFrame(
                {'w_05' + " {:.2f}".format(potential): w_05, 'Im' + " {:.2f}".format(potential): I_elected})

            # Concatenate the data for this RPM to the right of the combined_data DataFrame
            Levich_plotshow_data = pd.concat([Levich_plotshow_data, potential_data], axis=1)

            # Perform linear regression
            coeffs = np.polyfit(w_05, I_elected, 1)

            # Store the regression information
            Levich_slope_i = coeffs[0]
            Levich_intercept_i = coeffs[1]
            Levich_slope.append(Levich_slope_i)
            Levich_intercept.append(Levich_intercept_i)

            x_regression = np.linspace(min(w_05), max(w_05), 100)
            y_regression = np.polyval(coeffs, x_regression)

            B = np.abs(Levich_slope_i)
            F = 96485.3321
            D23 = B / (0.62 * n * F * A * (v ** -(1 / 6)) * C)
            D_i = D23 ** (3 / 2)

            D.append(D_i)

            # Plot the regression line
            plt.plot(x_regression, y_regression, label=f'{potential:.2f}V')

        plt.xlabel('$[Rotation Rate/(Rad/s)]^{1/2}$')
        plt.ylabel('Limit current/A')
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        plt.legend(loc='lower left')
        plt.grid()
        to_file1 = os.path.join(self.datapath, "HDV_step2_1_p1.png")
        plt.savefig(to_file1)

        to_file2 = os.path.join(self.datapath, "HDV_step2_1_Levich_plotshow_data.csv")
        Levich_plotshow_data.to_csv(to_file2, sep=',', index=False)
        return to_file1, to_file2


    def _step2_1_fig2(self, data, input_n=1, input_a = 1.0, input_v = 0.01, input_c = 0.000894454e-3 ):
        # Define constants and parameters_These are setting parameter
        start_value = -1.0  # Starting value of the range for potential
        end_value = 0.5  # Ending value of the range for potential
        interval = 100  # potential going to select every ?

        # These are calculation parameter
        n = input_n
        relectrode = 0.15  # Radius of the rotate electrode
        print('electrode Radius is :', relectrode, 'cm')
        A = np.pi * (relectrode ** 2)
        print('surface area is :', A, 'cm\u00b2')
        v = input_v  # kinematic viscosity of the solution (ν - cm2/s),
        C = input_c  # in mol/cm3

        # Load data
        # Levich_plotshow_data = pd.DataFrame()

        data = self.read_data()
        E = None
        for rpm, df in data.items():
            E = df['WE(1).Potential (V)']
            break

        # Calculate the corresponding indices within the range
        start_index = E[E >= start_value].idxmin()
        end_index = E[E <= end_value].idxmax()
        E_selected = E.iloc[start_index:end_index + 1]
        print('Number of Selected Potential:', len(E_selected))
        Levich_slope = []
        Levich_intercept = []
        D = []
        E_plot = []

        try:
            sigma = self.res_data['HDV']['form1']['input']['sigma']
        except Exception as e:
            sigma = 10.0

        for j in range(0, len(E_selected), interval):
            potential = E_selected.iloc[j]

            print('now processing', "index:", j, "E:", potential)
            w_05 = []
            Il = []

            for rpm, df in data.items():
                # x axis（w）
                w_i = rpm_to_rads(int(rpm.replace('rpm', '')))
                w05_i = w_i ** 0.5
                w_05.append(w05_i)

                # y axis (Ii)
                E_irpm = df['Potential applied (V)']
                I_irpm = df['WE(1).Current (A)']

                # Apply the Gaussian filter to the 'Current (A)'
                I_irpm = gaussian_filter(I_irpm, sigma=sigma)

                I_potential_i = find_y(E_irpm, I_irpm, potential)
                Il.append(I_potential_i)

            # Perform linear regression
            coeffs = np.polyfit(w_05, Il, 1)
            Bi = coeffs[0]
            intercept_i = coeffs[1]
            Levich_slope.append(Bi)
            Levich_intercept.append(intercept_i)
            E_plot.append(potential)

        # calculate D from B
        # check these parameter
        Levich_slope = np.array(Levich_slope)
        B = np.abs(Levich_slope)
        F = 96485.3321
        D23 = B / (0.62 * n * F * A * (v ** -(1 / 6)) * C)
        D = D23 ** (3 / 2)

        ig, ax1 = plt.subplots()

        # Scatter plot for the first y-axis
        ax1.scatter(E_plot, Levich_slope, s=2, color='#1f77b4')
        ax1.set_xlabel('Applied potential/V')
        ax1.set_ylabel('Corresponding Slope B', color='k')
        ax1.tick_params(axis='y', labelcolor='#1f77b4')

        # Create a second y-axis
        ax2 = ax1.twinx()

        # Scatter plot for the second y-axis
        ax2.scatter(E_plot, D, s=2, color='#ff7f0e')
        ax2.set_ylabel('Diffusion coefficient(D)/cm\u00b2/s', color='k')
        ax2.tick_params(axis='y', labelcolor='#ff7f0e')

        plt.grid()
        # plt.show()
        to_file1 = os.path.join(self.datapath, "HDV_step2_1_p2.png")
        plt.savefig(to_file1)

        return to_file1

    def step2_1(self, input_n=1, input_a = 1.0, input_v = 0.01, input_c = 0.000894454e-3):
        """ Step 2 """
        data = self.res_data
        to_file1, excel_file = self._step2_1_fig1(data, int(input_n), float(input_a), float(input_v), float(input_c))
        to_file2 = self._step2_1_fig2(data, int(input_n), float(input_a), float(input_v), float(input_c))

        if 'HDV' not in data.keys():
            data['HDV'] = {}
        data['HDV']['form2'] = {
            'status': 'done',
            'input': {
                'C': input_c,
                'A': input_a,
                'V': input_v,
                'N': input_n,
                'method': 1,
            },
            'output': {
                'file1': to_file1 if to_file1.startswith("/") else '/' + to_file1,
                'file2': to_file2 if to_file2.startswith("/") else '/' + to_file2,
                'excel_file': excel_file if excel_file.startswith("/") else '/' + excel_file,
                # 'img1': '/outputs/version_test_CV/form2.jpg',
            }
        }
        self.save_result_data(data)


    def step2_2(self, input_n=1, input_a = 1, input_v = 0.01, input_c = 0.000894454e-3):
        pass

if __name__ == '__main__':
    hdv = HDV('version_0423_111216', "uploads/version_0423_111216/fileinfo_version_0423_111216.json")
    # hdv.start()
    hdv.start2_1()

