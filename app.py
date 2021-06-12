#!/usr/bin/env python3

import csv
from data import control_variables
from printing import *
from math import log
import matplotlib.pyplot as plt
import numpy as np

def import_data():

    """Load data from csv file into 2d array and return to call site"""

    data = []

    with open("./data/measured_variables.csv", "r") as file:

        file_handle = csv.reader(file)
        for row in file_handle:

            numeric_data = [float(i) for i in row]
            data.append(numeric_data)

    return data

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

    # print_data(mass, abs_unc_mass, perc_unc_mass, control_variables.perc_unc_area)

    volume = make_cumulative_series(d_volume)
    volume = [i/(1E6) for i in volume] # convert to m^3

    force = [i * control_variables.gravity_acceleration for i in mass]
    perc_unc_force = perc_unc_mass
    # print_data(force, perc_unc_force)

    pressure = [i/control_variables.area for i in force]
    perc_unc_pressure = [i + control_variables.perc_unc_area for i in perc_unc_force]

    abs_unc_pressure = []
    for value, perc_uncertainty in zip(pressure, perc_unc_pressure):

        abs_unc_pressure.append((perc_uncertainty/100)*value)

    # print_data(pressure, perc_unc_pressure, abs_unc_pressure)
    # print_data(volume, control_variables.abs_unc_volume)

    log_pressure = [log(i, 10) for i in pressure]
    abs_unc_log_pressure = [log(i, 10) for i in abs_unc_pressure]
    # print_data(log_pressure, abs_unc_log_pressure)

    log_volume = [log(i, 10) for i in volume]
    abs_unc_log_volume = [log(control_variables.abs_unc_volume, 10) for _ in volume]
    # print_data(log_volume, abs_unc_log_volume)

    # graph plotting
    x = np.array(log_volume)
    y = np.array(log_pressure)
    # gradient, intercept = np.polyfit(x,y,1)
    # print_data(gradient, intercept)

    equation = np.polyfit(x,y,1)
    f = np.poly1d(equation)

    # for i in range(int(min(x)) - 2, int(max(x)) + 2):
    #     plt.plot(i, f(i), 'go')

    lower = int(min(x)) - 10
    upper = int(max(x)) + 10
    plt.plot((lower, upper), (f(lower), f(upper)), 'r')

    plt.plot(log_volume, log_pressure, 'o')
    # plt.plot(x, gradient*x + intercept)
    plt.errorbar(log_volume, log_pressure, yerr=abs_unc_log_pressure, xerr=abs_unc_log_volume, fmt=" ", ecolor="grey", elinewidth=1, capsize=5)
    plt.grid()
    plt.show()

if __name__ == "__main__":

    main()
