import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import functions
import config
from math import log
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

RESISTANCE = 68000
CAPACITANCE = 2200e-6
NUM_READINGS = 90

def main():

    raw_data = functions.import_data(config.in_dir+"capacitor.csv")
    t = [point[0] for point in raw_data]
    vt1 = [point[1] for point in raw_data]
    vt2 = [point[2] for point in raw_data]
    vt3 = [point[3] for point in raw_data]
    vtm = [functions.average_repeats(point[1:]) for point in raw_data]
    lvt = [log(point) for point in vtm]
    y = list(filter(lambda i: i >= 1, lvt))
    x = t[:len(y)]

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(8)
    ax = f.add_subplot(1,1,1)
    ax.set_xlim(0,300)
    ax.set_ylim(0,3)
    ax.spines['top'].set_color("#aaaaaa")
    ax.spines['right'].set_color("#aaaaaa")
    ax.spines['left'].set(linewidth=1.2)
    ax.spines['bottom'].set(linewidth=1.2)
    ax.xaxis.set_major_locator(MultipleLocator(50))
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    ax.yaxis.set_major_locator(MultipleLocator(0.5))
    ax.yaxis.set_minor_locator(AutoMinorLocator(4))
    # ax.axis("square")
    ax.tick_params(which='minor', width=1.2, length=4, color="#000000")
    ax.grid(which="minor", linewidth=1, color='#dddddd', zorder=-10, linestyle="--")
    ax.tick_params(which='major', width=1.2, length=10, color="#000000")
    ax.grid(which="major", linewidth=1.0, color='#aaaaaa', zorder=-10)
    ax.plot(x[1:-1:2], y[1:-1:2], marker="x", linestyle="None", markersize=7)

    equation = np.polyfit(x,y,1)
    f = np.poly1d(equation)
    print(f)
    lower = min(x)
    upper = max(x)
    ax.plot((lower, upper), (f(lower), f(upper)), color='grey', alpha=0.5)

    ax.set_title("Potential Differenct of a Capacitor Against Time", fontsize=10, verticalalignment='bottom')
    ax.set_xlabel("time (s)")
    ax.set_ylabel("ln(Vt)")
    plt.savefig(config.plot_dir+"capacitor.png")

    processed_data = {"time (s)": t, "Vt 1 (v)": vt1, "Vt 2 (v)": vt2, "Vt 3 (v)": vt3, "Vt mean (v)": vtm, "Ln(Vt mean)": lvt}
    functions.export_data(config.out_dir+"capacitor.csv", processed_data, NUM_READINGS, headings=False)

if __name__ == "__main__":
    main()
