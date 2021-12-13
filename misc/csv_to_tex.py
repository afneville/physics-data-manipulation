import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import functions
import config


raw_data = functions.import_data(config.out_dir+"capacitor.csv")
open_multicol = "\\multicolumn{1}{|r|}{"
for i in raw_data:
    print(open_multicol+str(int(i[0])), end="}&")
    for j in range(1, 5):
        print(open_multicol+"{:.2f}".format(i[j]), end="}&")
    print(open_multicol+"{:.2f}".format(i[5]), end="}\\\\\n")
    print("\\hline")
