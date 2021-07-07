import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import functions

from data import control_variables
from math import log
import matplotlib.pyplot as plt
import numpy as np

def main():

    # load data into lists
    raw_data = functions.import_data()
    volume = [functions.average_repeats(i[1:]) for i in raw_data]
    height = [i[0] for i in raw_data]

    volume = [i/1000 for i in volume]
    perc_unc_volume = [(control_variables.abs_unc_volume/i)*100 for i in volume]
    perc_unc_time = [(control_variables.abs_unc_time/20)*100 for _ in volume]
    flow_rate = [i/control_variables.time for i in volume]

    perc_unc_flow_rate = []
    for i, j in zip(perc_unc_volume, perc_unc_time):

        perc_unc_flow_rate.append(i + j)

    abs_unc_flow_rate = []
    for value, perc_uncertainty in zip(flow_rate, perc_unc_flow_rate):

        abs_unc_flow_rate.append((perc_uncertainty/100)*value)

    x = np.array(height)
    y = np.array(flow_rate)

    equation = np.polyfit(x,y,1)
    print(equation)
    f = np.poly1d(equation)

    # for i in range(int(min(x)) - 2, int(max(x)) + 2):
    #     plt.plot(i, f(i), 'go')

    lower = min(x)
    upper = max(x)

    figure = plt.figure()
    graph = figure.add_subplot(1,1,1)
    graph.set_title("Flow rate against vertical displacement")
    graph.set_xlabel("height (m)", fontweight="bold", loc="left")
    graph.set_ylabel("rate (m^3/s)", fontweight="bold", loc="top")
    graph.plot(height, flow_rate, 'o')
    graph.errorbar(height, flow_rate, yerr=abs_unc_flow_rate, xerr=control_variables.abs_unc_height, fmt=" ", ecolor="grey", elinewidth=1, capsize=5)
    graph.plot((lower, upper), (f(lower), f(upper)), color='grey', alpha=0.5)

    plt.show()

    processed_data = {"height (m)": height,
        "volume (m^3)": volume,
        "flow rate": flow_rate,
        "perc. unc. volume": perc_unc_volume,
        "perc. unc. flow_rate": perc_unc_flow_rate}

    functions.export_data(processed_data, control_variables.num_readings)

if __name__ == "__main__":

    main()
