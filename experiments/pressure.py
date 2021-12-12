#!/usr/bin/env python3

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import functions
import config
from math import log
from math import pi
import matplotlib.pyplot as plt
import numpy as np

DIAMETER = 0.0284
ABS_UNC_DIAMETER = 0.0001
AREA = pi*(DIAMETER/2)**2
PERC_UNC_AREA = ((ABS_UNC_DIAMETER/DIAMETER) * 100)*2
NUM_READINGS = 6
ABS_UNC_MASS = [0.0001 for _ in range(NUM_READINGS)]
ABS_UNC_VOLUME = 2/(1E6)
GRAVITY_ACCELERATION = 9.81

def calculate_pressure(force, perc_unc_force):
    """Calculate pressure with associated absolute uncertainty"""

    pressure = [i/AREA for i in force]
    perc_unc_pressure = [i + PERC_UNC_AREA for i in perc_unc_force]
    abs_unc_pressure = []
    for value, perc_uncertainty in zip(pressure, perc_unc_pressure):
        abs_unc_pressure.append((perc_uncertainty/100)*value)

    return pressure, perc_unc_pressure

def main():

    raw_data = functions.import_data(config.in_dir+"pressure.csv")
    d_mass = [i[0] for i in raw_data]
    d_volume = [functions.average_repeats(i[1:]) for i in raw_data]
    mass = functions.make_cumulative_series(d_mass)
    abs_unc_mass = functions.make_cumulative_series(ABS_UNC_MASS)
    perc_unc_mass = []
    for value, abs_unc in zip(mass, abs_unc_mass):
        perc_unc_mass.append((abs_unc/value)*100)
    volume = functions.make_cumulative_series(d_volume)
    volume = [i/(1E6) for i in volume] # convert to m^3
    force = [i * GRAVITY_ACCELERATION for i in mass]
    perc_unc_force = perc_unc_mass
    pressure = [i/AREA for i in force]
    perc_unc_pressure = [i + PERC_UNC_AREA for i in perc_unc_force]
    abs_unc_pressure = []
    for value, perc_uncertainty in zip(pressure, perc_unc_pressure):
        abs_unc_pressure.append((perc_uncertainty/100)*value)
    log_pressure = [log(i, 10) for i in pressure]
    abs_unc_log_pressure = [log(i, 10) for i in abs_unc_pressure]
    log_volume = [log(i, 10) for i in volume]
    abs_unc_log_volume = [log(ABS_UNC_VOLUME, 10) for _ in volume]

    x = np.array(log_volume)
    y = np.array(log_pressure)
    equation = np.polyfit(x,y,1)
    f = np.poly1d(equation)
    lower = int(min(x)) - 10
    upper = int(max(x)) + 10

    figure = plt.figure()
    graph = figure.add_subplot(1,1,1)
    graph.set_title("log(p) against log(v)")
    graph.set_xlabel("log(v)", fontweight="bold", loc="left")
    graph.set_ylabel("log(p)", fontweight="bold", loc="top")
    graph.plot(log_volume, log_pressure, 'o')
    graph.errorbar(log_volume, log_pressure, yerr=abs_unc_log_pressure,
                   xerr=abs_unc_log_volume, fmt=" ", ecolor="grey",
                   elinewidth=1, capsize=5)
    graph.plot((lower, upper), (f(lower), f(upper)), color='grey', alpha=0.5)
    plt.grid(b=True, which='major',
            color ='#000000', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', 
            color='#999999', linestyle='-', alpha=0.2)
    graph.spines.left.set_position('zero')
    graph.spines.right.set_color('none')
    graph.spines.bottom.set_position('zero')
    graph.spines.top.set_color('none')
    graph.xaxis.set_ticks_position('bottom')
    graph.yaxis.set_ticks_position('left') 
    plt.savefig(config.plot_dir+"pressure.png")

    processed_data = {"mass (kg)":mass, "force (N)":force,
                      "perc. unc. force":perc_unc_force,
                      "pressure (pa)":pressure,
                      "perc. unc. pressure":perc_unc_pressure,
                      "abs. unc. pressure (+-pa)":abs_unc_pressure,
                      "volume (m^3)":volume, "log pressure":log_pressure,
                      "abs. unc. log pressure":abs_unc_log_pressure,
                      "log_volume":log_volume, "abs. unc. log volume":abs_unc_log_volume}
    functions.export_data(config.out_dir+"pressure.csv", processed_data, NUM_READINGS)

if __name__ == "__main__":

    main()
