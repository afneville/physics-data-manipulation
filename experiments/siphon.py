import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import functions
import config

import matplotlib.pyplot as plt
import numpy as np

ABS_UNC_VOLUME = 0.1/1000
ABS_UNC_HEIGHT = 0.01
TIME = 20
ABS_UNC_TIME = 1
NUM_READINGS = 5

def main():

    raw_data = functions.import_data(config.in_dir+"siphon.csv")
    volume = [functions.average_repeats(i[1:]) for i in raw_data]
    height = [i[0] for i in raw_data]
    volume = [i/1000 for i in volume]

    perc_unc_volume = [(ABS_UNC_VOLUME/i)*100 for i in volume]
    perc_unc_time = [(ABS_UNC_TIME/20)*100 for _ in volume]
    flow_rate = [i/TIME for i in volume]
    perc_unc_flow_rate = []
    for i, j in zip(perc_unc_volume, perc_unc_time):
        perc_unc_flow_rate.append(i + j)
    abs_unc_flow_rate = []
    for value, perc_uncertainty in zip(flow_rate, perc_unc_flow_rate):
        abs_unc_flow_rate.append((perc_uncertainty/100)*value)

    x = np.array(height)
    y = np.array(flow_rate)
    equation = np.polyfit(x,y,1)
    f = np.poly1d(equation)
    lower = min(x)
    upper = max(x)

    figure = plt.figure()
    graph = figure.add_subplot(1,1,1)
    graph.set_title("Flow rate against vertical displacement")
    graph.set_xlabel("height (m)", fontweight="bold", loc="left")
    graph.set_ylabel("rate (m^3/s)", fontweight="bold", loc="top")
    graph.plot(height, flow_rate, 'o')
    graph.errorbar(height, flow_rate, yerr=abs_unc_flow_rate, xerr=ABS_UNC_HEIGHT, fmt=" ", ecolor="grey", elinewidth=1, capsize=5)
    graph.plot((lower, upper), (f(lower), f(upper)), color='grey', alpha=0.5)
    plt.savefig(config.plot_dir+"siphon.png")

    processed_data = {"height (m)": height,
        "volume (m^3)": volume,
        "flow rate": flow_rate,
        "perc. unc. volume": perc_unc_volume,
        "perc. unc. flow_rate": perc_unc_flow_rate}
    functions.export_data(config.out_dir+"siphon.csv", processed_data, NUM_READINGS)

if __name__ == "__main__":
    main()
