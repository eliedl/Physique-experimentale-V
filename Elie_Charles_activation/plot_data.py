import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


gauss = lambda x, mu, sig, A:  A / (sig * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sig ** 2))

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
    indexes = np.linspace(0,len(data)-1,len(data))
    print(filename)
    plt.plot(data, linewidth = 0.5)
    for peak_indexes in file_peaks[count]:
        popt, pcov = curve_fit(gauss, range(peak_indexes[1]-peak_indexes[0]), data[peak_indexes[0]:peak_indexes[1]])
        fit_mu, fit_stdev, fit_ampl= popt
        FWHM = 2 * np.sqrt(2 * np.log(2)) * fit_stdev
        plt.plot(indexes[peak_indexes[0]:peak_indexes[1]], gauss( np.arange(peak_indexes[1]-peak_indexes[0]), fit_mu, fit_stdev, fit_ampl))

    plt.show()
    count += 1
