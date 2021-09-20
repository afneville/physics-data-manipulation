
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from data import control_variables
import functions
import numpy as np
import matplotlib.pyplot as plt
import math

def main():
    raw_data = functions.import_data()
    functions.print_data(raw_data)

    distance = [i[0] for i in raw_data]
    height =   [i[1] for i in raw_data]

    functions.print_data(distance, height)

    recip_d = [1/math.sqrt(i) for i in distance]
    recip_h = [(1/i*1) for i in height]

    x = np.array(recip_d)
    y = np.array(height)

    equation = np.polyfit(x,y,1)
    print(equation)
    f = np.poly1d(equation)

    # for i in range(int(min(x)) - 2, int(max(x)) + 2):
    #     plt.plot(i, f(i), 'go')

    lower = min(x)
    upper = max(x)

    figure = plt.figure()
    graph = figure.add_subplot(1,1,1)

    plt.grid(b=True, which='major', color ='#000000', linestyle='-')
    plt.minorticks_on()
    plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)

    # graph.spines.left.set_position('zero')
    # graph.spines.right.set_color('none')
    # graph.spines.bottom.set_position('zero')
    # graph.spines.top.set_color('none')
    graph.xaxis.set_ticks_position('bottom')
    graph.yaxis.set_ticks_position('left') 
    graph.set_title("height against 1/ root distance to card.")
    graph.set_xlabel("1/ root distance (m)", fontweight="bold", loc="left")
    graph.set_ylabel("height (m)", fontweight="bold", loc="top")
    graph.plot(recip_d, height, 'x')
    graph.plot((lower, upper), (f(lower), f(upper)), color='grey', alpha=0.5)

    plt.show()

if __name__ == "__main__":
    main()
