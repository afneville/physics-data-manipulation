import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import functions

from data import control_variables
from math import log

import numpy as np
import matplotlib.pyplot as plt

def main():
    raw_data = functions.import_data()
    t = [point[0] for point in raw_data]
    vt = [functions.average_repeats(point[1:]) for point in raw_data]
    lvt = [log(point) for point in vt]
    lvt = list(filter(lambda i: i >= 1, lvt))
    t = t[:len(lvt)]
    # functions.print_data(lvt)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    ax.plot(t, lvt, "x", mfc = "b", mec = "b", color = "k")
    plt.ylim(ymin=0, ymax=3)
    plt.xlim(xmin=0, xmax=300)
    ax.grid(linewidth=1, alpha=0.8, which='both')
    plt.savefig("fig.png")

if __name__ == "__main__":
    main()
