import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import functions
import config
from math import log
import numpy as np
import matplotlib.pyplot as plt

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
    x = t[:len(lvt)]

    processed_data = {"time (s)": t, "Vt 1 (v)": vt1, "Vt 2 (v)": vt2, "Vt 3 (v)": vt3, "Vt mean (v)": vtm, "Ln(Vt mean)": lvt}
    functions.export_data(config.out_dir+"capacitor.csv", processed_data, NUM_READINGS)

if __name__ == "__main__":
    main()
