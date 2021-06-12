#!/usr/bin/env python3

import csv
from pprint import pprint
from data import control_variables
from math import log
import matplotlib.pyplot as plt
import numpy as np

class Counter():

    """keep track of function calls"""

    def __init__(self, f):

        self._f = f
        self._uses = 0

    def __call__(self, *args):

        self._uses += 1
        print(f"\nnum_uses: {self._uses}\n")

        self._f(args)


@Counter
def print_data(*args):

    """pprint all the input data"""

    for i in args[0]:

        pprint(i)

def import_data():

    """Load data from csv file into 2d array and return to call site"""

    data = []

    with open("./data/measured_variables.csv", "r") as file:

        file_handle = csv.reader(file)
        for row in file_handle:

            numeric_data = [float(i) for i in row]
            data.append(numeric_data)

    return data

def export_data(data):

    """ given a dictionary containing lists of data, write data to a csv file """

    with open("./data/processed_data.csv", "w") as file:

        file_handle = csv.writer(file)
        columns = [key for key in data]
        file_handle.writerow(columns)

        for i in range(control_variables.num_readings):

            row = []
            for key in columns:
                row.append(data[key][i])

            file_handle.writerow(row)

def average_repeats(repeats):

    """Average the repeat readings of volume taken during the experiment"""

    return sum(repeats) / len(repeats)

def make_cumulative_series(x):

    """Find the cumulative totals of a series, useful for graph plotting"""

    cumulative_totals = []
    sum_x = 0 
    for i in x:
        sum_x += i 
        cumulative_totals.append(sum_x)

    return cumulative_totals

def calculate_pressure(force, perc_unc_force):

    """Calculate pressure with associated absolute uncertainty"""

    # calculate pressure for each mass that is added
    pressure = [i/control_variables.area for i in force]

    # calculate the percentage uncertainty in pressure by adding percentage uncertainty of each constituent
    perc_unc_pressure = [i + control_variables.perc_unc_area for i in perc_unc_force]
    abs_unc_pressure = []

    for value, perc_uncertainty in zip(pressure, perc_unc_pressure):

        abs_unc_pressure.append((perc_uncertainty/100)*value)

    return pressure, perc_unc_pressure

def main():

    raw_data = import_data()

    d_mass = [i[0] for i in raw_data]
    d_volume = [average_repeats(i[1:]) for i in raw_data]

    mass = make_cumulative_series(d_mass)
    abs_unc_mass = make_cumulative_series(control_variables.abs_unc_mass)

    perc_unc_mass = []
    for value, abs_unc in zip(mass, abs_unc_mass):

        perc_unc_mass.append((abs_unc/value)*100)

    volume = make_cumulative_series(d_volume)
    volume = [i/(1E6) for i in volume] # convert to m^3

    force = [i * control_variables.gravity_acceleration for i in mass]
    perc_unc_force = perc_unc_mass

    pressure = [i/control_variables.area for i in force]
    perc_unc_pressure = [i + control_variables.perc_unc_area for i in perc_unc_force]

    abs_unc_pressure = []
    for value, perc_uncertainty in zip(pressure, perc_unc_pressure):

        abs_unc_pressure.append((perc_uncertainty/100)*value)


    log_pressure = [log(i, 10) for i in pressure]
    abs_unc_log_pressure = [log(i, 10) for i in abs_unc_pressure]

    log_volume = [log(i, 10) for i in volume]
    abs_unc_log_volume = [log(control_variables.abs_unc_volume, 10) for _ in volume]

    # best fit line
    x = np.array(log_volume)
    y = np.array(log_pressure)

    # gradient, intercept = np.polyfit(x,y,1)
    equation = np.polyfit(x,y,1)
    f = np.poly1d(equation)

    # for i in range(int(min(x)) - 2, int(max(x)) + 2):
    #     plt.plot(i, f(i), 'go')

    lower = int(min(x)) - 10
    upper = int(max(x)) + 10

    # ploting data

    figure = plt.figure()
    graph = figure.add_subplot(1,1,1)
    graph.set_title("log(p) against log(v)")
    graph.set_xlabel("log(v)", fontweight="bold", loc="left")
    graph.set_ylabel("log(p)", fontweight="bold", loc="top")
    graph.plot(log_volume, log_pressure, 'o')
    graph.errorbar(log_volume, log_pressure, yerr=abs_unc_log_pressure, xerr=abs_unc_log_volume, fmt=" ", ecolor="grey", elinewidth=1, capsize=5)
    graph.plot((lower, upper), (f(lower), f(upper)), color='grey', alpha=0.5)

    plt.grid(b=True, which='major', color ='#000000', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

    graph.spines.left.set_position('zero')
    graph.spines.right.set_color('none')
    graph.spines.bottom.set_position('zero')
    graph.spines.top.set_color('none')
    graph.xaxis.set_ticks_position('bottom')
    graph.yaxis.set_ticks_position('left') 

    plt.show()

    processed_data = {"mass (kg)":mass,"force (N)":force,"perc. unc. force":perc_unc_force,"pressure (pa)":pressure,"perc. unc. pressure":perc_unc_pressure,"abs. unc. pressure (+-pa)":abs_unc_pressure,"volume (m^3)":volume,"log pressure":log_pressure,"abs. unc. log pressure":abs_unc_log_pressure,"log_volume":log_volume,"abs. unc. log volume":abs_unc_log_volume}
    export_data(processed_data)

if __name__ == "__main__":

    main()
