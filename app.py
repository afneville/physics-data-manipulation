#!/usr/bin/env python3

import csv
from data import control_variables
from printing import *

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
    volume = make_cumulative_series(d_volume)
    volume = [i/(1E6) for i in volume]

    perc_unc_mass = [(control_variables.abs_unc_mass/i)*100 for i in mass]
    perc_unc_force = perc_unc_mass

    force = [i * control_variables.gravity_acceleration for i in mass]
    pressure, abs_unc_pressure = calculate_pressure(force, perc_unc_force)


if __name__ == "__main__":

    main()
