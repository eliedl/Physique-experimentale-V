import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

gauss = lambda x, mu, sig, A: A / (sig * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sig ** 2))

cwd = os.getcwd()
datawd = cwd + "\\Données\\Pydata\\"
filename = "etalonnage_canaux_python.npy"
file_peaks = [(215, 273), (1092, 1272), (1958, 2145), (2225, 2441)]  # etalonnage_canaux_python.npy
peak_energies = [122, 662, 1170, 1330]
data = np.load(datawd + filename)
indexes = np.linspace(0, len(data) - 1, len(data))
print(filename)
plt.plot(data, linewidth=0.5)
plt.xlabel("Channel")
plt.ylabel("Count")
means, stdevs, ampls, perrs, FWHMs= [],[],[],[], []
for peak_indexes in file_peaks:
    popt, pcov = curve_fit(gauss, range(peak_indexes[1] - peak_indexes[0]), data[peak_indexes[0]:peak_indexes[1]])
    fit_mu, fit_stdev, fit_ampl = popt
    perr = np.sqrt(np.diag(pcov))
    FWHM = 2 * np.sqrt(2 * np.log(2)) * fit_stdev
    plt.plot(indexes[peak_indexes[0]:peak_indexes[1]],
             gauss(np.arange(peak_indexes[1] - peak_indexes[0]), fit_mu, fit_stdev, fit_ampl), c = "red")

    means.append(fit_mu + peak_indexes[0])
    stdevs.append(fit_stdev)
    ampls.append(fit_ampl)
    perrs.append(perr)
    FWHMs.append(FWHM)

plt.show()
line = lambda x, a, b: a*x + b
popt, pcov = curve_fit(line, means, peak_energies)
perr = np.sqrt(np.diag(pcov))

plt.plot(indexes,line(indexes, popt[0], popt[1]),'--',c= "black", linewidth = 1)
plt.plot(means,peak_energies,'o',c = "black")
plt.text(0,0,"Droite :y = {}x + {}, erreur = {}".format(np.round(popt[0], 3),np.round(popt[1], 3), np.round(perr[1],3)))
plt.xlabel("Channel")
plt.ylabel("Énergie [KeV]")
plt.show()
plt.plot(line(indexes, popt[0], popt[1]),data, linewidth=0.5)
plt.xlabel("Énergie [KeV]")
plt.ylabel("Count")
plt.show()