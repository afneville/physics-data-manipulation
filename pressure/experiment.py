#!/usr/bin/env python3

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import functions

from data import control_variables
from math import log
import matplotlib.pyplot as plt
import numpy as np


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

    raw_data = functions.import_data()

    d_mass = [i[0] for i in raw_data]
    d_volume = [functions.average_repeats(i[1:]) for i in raw_data]

    mass = functions.make_cumulative_series(d_mass)
    abs_unc_mass = functions.make_cumulative_series(control_variables.abs_unc_mass)

    perc_unc_mass = []
    for value, abs_unc in zip(mass, abs_unc_mass):

        perc_unc_mass.append((abs_unc/value)*100)

    volume = functions.make_cumulative_series(d_volume)
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
    print(equation)
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

    processed_data = {"mass (kg)":mass,
                      "force (N)":force,
                      "perc. unc. force":perc_unc_force,
                      "pressure (pa)":pressure,
                      "perc. unc. pressure":perc_unc_pressure,
                      "abs. unc. pressure (+-pa)":abs_unc_pressure,
                      "volume (m^3)":volume,
                      "log pressure":log_pressure,
                      "abs. unc. log pressure":abs_unc_log_pressure,
                      "log_volume":log_volume,
                      "abs. unc. log volume":abs_unc_log_volume}

    functions.export_data(processed_data, control_variables.num_readings)

if __name__ == "__main__":

    main()
