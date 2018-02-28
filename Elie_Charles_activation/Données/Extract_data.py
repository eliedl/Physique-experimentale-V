import os
import numpy as np

cwd = os.getcwd()
files = os.listdir(cwd)
datafiles = []
for filename in files:
    if filename[-4:] == ".Spe":
        file = open(filename,'r')
        lines = file.readlines()
        char_data = np.array(lines[12:4107])
        data = np.ndarray.astype(char_data,int)
        np.save("Pydata\\" + filename[:-4] + "_python", data)
