import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
def run_etalonnage(nb_sigmas = 1):
    gauss = lambda x, mu, sig, A: A / (sig * np.sqrt(2 * np.pi)) * np.exp(-(x - mu) ** 2 / (2 * sig ** 2))

    cwd = os.getcwd()
    datawd = cwd + "\\Données\\Pydata\\"
    filename = "etalonnage_canaux_python.npy"
    file_peaks = [(215, 273), (1092, 1272), (1958, 2145), (2225, 2441)]  # etalonnage_canaux_python.npy
    peak_energies = [122, 662, 1170, 1330]
    peak_names = ["$\ ^{60}Co$","$\ ^{60}Co$","$\ ^{137}Cs$","$\ ^{57}Co$"]
    data = np.load(datawd + filename)
    indexes = np.linspace(0, len(data) - 1, len(data))
    plt.plot(data, 'o', ms = 0.5, c = "black",label = "Compte de photons")
    plt.xlabel("Canal")
    plt.ylabel("Nombre de photons")
    plt.grid(True)
    means, stdevs, ampls, perrs, FWHMs= [],[],[],[], []
    count = -1
    for peak_indexes in file_peaks:
        count += 1
        popt, pcov = curve_fit(gauss, range(peak_indexes[1] - peak_indexes[0]), data[peak_indexes[0]:peak_indexes[1]])
        fit_mu, fit_stdev, fit_ampl = popt
        perr = np.sqrt(np.diag(pcov))
        FWHM = 2 * np.sqrt(2 * np.log(2)) * fit_stdev
        if count == 1:
            plt.plot(indexes[peak_indexes[0]:peak_indexes[1]],
                     gauss(np.arange(peak_indexes[1] - peak_indexes[0]), fit_mu, fit_stdev, fit_ampl), c = "red", alpha = 0.75, label = "fit Gaussien")
        else:
            plt.plot(indexes[peak_indexes[0]:peak_indexes[1]],
                     gauss(np.arange(peak_indexes[1] - peak_indexes[0]), fit_mu, fit_stdev, fit_ampl), c="red", alpha=0.75)

        plt.text(fit_mu + peak_indexes[0] + 100,data[int(np.round(fit_mu)) + peak_indexes[0]] - 100, "Pic de {} à {} KeV \n $\mu$: {}   $\sigma$ : {} \n".format(peak_names[count], peak_energies[count], int(np.round(fit_mu)) + peak_indexes[0], np.round(fit_stdev,3)))
        means.append(fit_mu + peak_indexes[0])
        stdevs.append(fit_stdev)
        ampls.append(fit_ampl)
        perrs.append(perr)
        FWHMs.append(FWHM)
    plt.legend()
    #plt.show()
    line = lambda x, a, b: a*x + b
    plt.plot(means,peak_energies,'o',c = "red", alpha = 0.75, label = "Énergie du pic détecté au canal")
    plt.errorbar(means,peak_energies, xerr=np.array(stdevs)*nb_sigmas, fmt = '.',c = "red", alpha = 0.75)
    text = ["supérieur", "moyen", "inférieur"]
    droites = []
    for i in range(3):
        popt, pcov = curve_fit(line, means + (1 - i)*nb_sigmas*np.array(stdevs), peak_energies)
        perr = np.sqrt(np.diag(pcov))
        droites.append(popt)
        if i == 1:
            plt.text(893, 27, "Droite :y = {}x + {}, erreur = {}".format(np.round(popt[0], 3), np.round(popt[1], 3),
                                                                         np.round(perr[1], 3)))
        plt.plot(indexes,line(indexes, popt[0], popt[1]),'--',c= "black", linewidth = 1, label = "Fit linéaire {}".format(text[i]), alpha = 0.5 + (1 - abs((1 - i)))*0.5)
    plt.xlabel("Canal")
    plt.ylabel("Énergie [KeV]")
    plt.legend()
    #plt.show()
    plt.plot(line(indexes, popt[0], popt[1]),data, 'o', ms = 0.5, c = "black",label = "Compte de photons")
    plt.xlabel("Énergie [KeV]")
    plt.ylabel("Count")
    #plt.show()
    return droites