#!/usr/bin/env python3

import csv
from pprint import pprint
from data import control_variables

def import_data():

    """ load data from csv file into 2d array and return to call site """

    data = []

    with open("./data/boyles_law_data.csv", "r") as file:

        file_handle = csv.reader(file)
        for row in file_handle:

            numeric_data = [float(i) for i in row]
            data.append(numeric_data)

    return data

def display_raw_data(raw_data):

    """ display input data for debugging """

    print(control_variables.diameter)
    print(control_variables.area)
    print(control_variables.perc_unc_area)
    raw_data[0][1:]
    pprint(raw_data)

def average_repeats(repeats):

    """ average the repeat readings of volume taken during the experiment """

    return sum(repeats) / len(repeats)

def main():

    raw_data = import_data()
    # display_raw_data(raw_data)


    averaged_data = [[i[0], average_repeats(i[1:])] for i in raw_data]
    # pprint(averaged_data)

if __name__ == "__main__":

    main()
