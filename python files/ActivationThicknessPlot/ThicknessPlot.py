#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import json
import collections
import itertools


def superscript(x):
    # Latex style superscript
    return "${}^{" + str(x) + "}$"


def format_isotope(X):
    # Formats an isotope name in latex
    if X == "triton":
        return X
    else:
        sym = ''
        A_num = ''
        for char in X:
            if char.isdigit():
                A_num += char
            else:
                sym += char
        return superscript(A_num) + sym


def saturation(n, error, lifeTime, beam_time=60):
    # returns the 1 min saturated *ACTIVITY*
    sat_act = n * (1 - np.exp(-beam_time/lifeTime)) / beam_time
    sat_err = error * (1 - np.exp(-beam_time/lifeTime)) / beam_time
    return sat_act, sat_err

MeV = 1e-3
kBq = 1e3
actual_protons = 1e11
isotopes_we_care_about = ["Be7", "C10", "C11", "O15", "O14", "N13", "N16", "F17", "F18", "Be11", "N17", "C15"]

outName = "ThicknessPlot.pdf"
fileNames = ["rangeshifter_t1_", "rangeshifter_t2_", "rangeshifter_t3_", "rangeshifter_t5_"]
phys_list = ["BIC", "BERT", "HADROTHE"]
names = ["Geant4 Binary cascade", "Geant4 Bertini cascade", "FLUKA Hadrotherapy"]
extension = ".json"
runs = [13, 13, 5]

ist_d = ["C11", "O15"]
energy = 200 * MeV

fig, ax = plt.subplots(1, 2, figsize=(10, 4))

for i, ist in enumerate(ist_d):
    for phys, name, run in zip(phys_list, names, runs):
        x = []
        y = []
        e = []
        for fileName in fileNames:
            fileName = fileName + phys + extension
            print("processing " + fileName)
            with open(fileName) as f:
                data = json.load(f)

            # Get number produced in run
            n = data[run]["isotopes"][ist]["number"]
            if n == 0:
                raise KeyError

            # Normalise to 10^11 protons
            normalised_n = n * actual_protons / data[run]["nEvents"]

            # Error in normalized N
            normalised_error = np.sqrt(n) * actual_protons / data[run]["nEvents"]

            # Get saturation activity & error
            r_act, r_act_error = saturation(
                n=normalised_n,
                error=normalised_error,
                lifeTime=data[run]["isotopes"][ist]["lifeTime"]
            )

            x.append(data[run]["rangeshifterThickness"])
            y.append(r_act / kBq)
            e.append(r_act_error / kBq)

        ax[i].set_xlim(0,6)
        ax[i].set_ylim(0,600)
        ax[i].set_xticks(np.arange(0,7,1))
        ax[i].errorbar(x, y, yerr=e, fmt=' ', c='k', capsize=4, elinewidth=1, zorder=10)


        # Plot regression
        x_f = np.linspace(0,6,5)
        f = lambda s: s * (y[-1] - y[0])/4 + y[0] - x[0] * (y[-1] - y[0])/4
        y_f = f(x_f)

        ax[i].plot(x_f, y_f, label=name)

    ax[i].set_ylabel("Activity of {} at the end of bombardment (kBq)".format(format_isotope(ist)))
    ax[i].set_xlabel("Range shifter thickness (cm)")


plt.legend()
plt.subplots_adjust(wspace=0.2)
plt.savefig(outName, bbox_inches = 'tight', pad_inches = 0)
