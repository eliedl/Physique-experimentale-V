from Elie_Charles_activation.etallonage import run_etalonnage
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

etallonage = run_etalonnage()
line = lambda x, params: params[0] * x + params[1]




cwd = os.getcwd()
datawd  = cwd + "\\Données\\Pydata\\"
files = os.listdir(datawd)
file_peaks = [[(2873,3227)], #aluminium_python.npy
              [(1039, 1239)],#argent_108_python.npy
              [(1029, 1266)],#argent_110_python.npy
              [],#bruit_aluminium_python.npy
              [], #bruit_argent_108_python.npy
              [],#bruit_cuivre_python.npy
              [], #bruit_vanadium_python.npy
              [(830,993), (1747, 1874)],#cuivre_python.npy
              [(215,273),(1092, 1272),(1958, 2145),(2225, 2441)],#etalonnage_canaux_python.npy
              [], #etalonnage_energie_python.npy
              [(2319,2615)]] #vanadium_python.npy

count = 0
for filename in files:
    data = np.load(datawd + filename)
    indexes = np.linspace(0, len(data) - 1, len(data))
    errors = [np.abs(line(indexes,etallonage[1]) - line(indexes, etallonage[0])),np.abs( line(indexes,etallonage[1]) - line(indexes, etallonage[2]))]
    error = np.amax(errors,0)
    print(error)
    #plt.errorbar(line(indexes,etallonage[1]), data, xerr=error, linewidth = 0.5, fmt = 'o', c = "black", ms = 0.5 )
    plt.errorbar(line(indexes,etallonage[1]), data, xerr=error, linewidth = 0.5, fmt = 'o', c = "black", ms = 0.5 )

    plt.show()
    count += 1
    break
