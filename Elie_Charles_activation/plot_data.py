from Elie_Charles_activation.etallonage import run_etalonnage
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

etallonage = run_etalonnage()
line = lambda x, params: params[0] * x + params[1]

gauss = lambda x, mu, sig, A:  A / (sig * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sig ** 2))

peak_names = ["Aluminium", "Argent 108", "Cuivre", "Cuivre", "Vanadium"]

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
plotcount = 0
allmeans, allstdevs, allampls, allperrs, allFWHMs = [], [], [], [], []

for filename in files:
    data = np.load(datawd + filename)
    try:
        bruit = np.load(datawd + "bruit_" + filename)
        filtered = np.abs(data - bruit)
        print("")
        print(filename)
    except:
        count += 1
        continue
    indexes = np.linspace(0,len(data)-1,len(data))
    errors = [np.abs(line(indexes,etallonage[1]) - line(indexes, etallonage[0])),np.abs( line(indexes,etallonage[1]) - line(indexes, etallonage[2]))]
    errors = np.amax(errors,0)
    plt.plot(line(indexes,etallonage[1]), data,'o', ms = 0.5,c = "black")
    #plt.plot(line(indexes,etallonage[1]), filtered, linewidth = 0.5)
    means, stdevs, ampls, perrs, FWHMs = [],[],[],[],[]
    for peak_indexes in file_peaks[count]:
        popt, pcov = curve_fit(gauss, range(peak_indexes[1]-peak_indexes[0]), data[peak_indexes[0]:peak_indexes[1]])
        fit_mu, fit_stdev, fit_ampl= popt
        FWHM = 2 * np.sqrt(2 * np.log(2)) * fit_stdev
        plt.plot(line(indexes[peak_indexes[0]:peak_indexes[1]],etallonage[1]), gauss( np.arange(peak_indexes[1]-peak_indexes[0]), fit_mu, fit_stdev, fit_ampl),c = "red" , alpha = 0.7)

        plt.text(int(np.round(line(fit_mu + peak_indexes[0],etallonage[1]))),data[int(np.round(fit_mu)) + peak_indexes[0]] , "Isotope de {} \n $\mu$: {}   $\epsilon_{{etalon.}}$ : {} \n".format(peak_names[plotcount], np.round(line(fit_mu + peak_indexes[0],etallonage[1])),  np.round(errors[int(np.round(fit_mu + peak_indexes[0]))])))

        means.append(fit_mu + peak_indexes[0])
        stdevs.append(fit_stdev)
        ampls.append(fit_ampl)
        FWHMs.append(FWHM)
    allmeans.append(means)
    allstdevs.append(stdevs)
    allampls.append(ampls)
    allFWHMs.append(FWHMs)
    for mean in means:
        print("     energie moyenne : ",np.round(line(mean,etallonage[1])), "error_etal = {}".format(np.round(errors[int(np.round(mean))])))
    plt.show()
    count += 1
    plotcount += 1
