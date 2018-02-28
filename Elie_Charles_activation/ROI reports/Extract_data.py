import os
import numpy as np

cwd = os.getcwd()
files = os.listdir(cwd)
datafiles = []
for filename in files:
    if filename[-4:] == ".Rpt":
        file = open(filename,'r')
        lines = file.readlines()
        char_data = np.array(lines[5:])
        array = []
        for i in char_data:
            array.append(i.split(' '))
        data = []
        for j in range(len(array[:])):
            for i in array[j]:
                if i != '':
                    try:
                        data.append(float(i))
                    except:
                        pass
        np.save("Pydata\\" + filename[:-4] + "_python", data)

