import csv

def import_data(path):

    """Load data from csv file into 2d array and return to call site"""

    data = []

    with open(path, "r") as file:

        file_handle = csv.reader(file)
        for row in file_handle:

            numeric_data = [float(i) for i in row]
            data.append(numeric_data)

    return data

def export_data(path, data, num_readings):

    """ given a dictionary containing lists of data, write data to a csv file """

    with open(path, "w") as file:

        file_handle = csv.writer(file)
        columns = [key for key in data]
        file_handle.writerow(columns)

        for i in range(num_readings):

            row = []
            for key in columns:
                row.append(data[key][i])

            file_handle.writerow(row)


