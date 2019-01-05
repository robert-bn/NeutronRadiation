# Plots ratios between Fluka, Binary Cascade and Bertini Cascade for each isotope
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


actual_protons = 1e11
isotopes_we_care_about = ["Be7", "C10", "C11", "O15", "O14", "N13", "N16", "F17", "F18", "Be11", "N17", "C15"]

def ratio_plot(
    fileNames,
    outName,
    outDir="pdfs/",
    title="",
    ymin=0,
    ymax=5,
    xlim=(70,250),
    fLabels=None,
    exclude=None,
    include=None,
    include_only=None,
    figSize=(10.5, 14.85),
    noIstLabels=False,
    loglog=False,
    log=True,
    bbox=(0.5, 0.5, 0.5, 0.5)):

    isotopes = isotopes_we_care_about.copy()

    if(exclude is not None):
        assert type(exclude) is list, "exclude keyword argument must be a list."
        for ist in exclude:
            isotopes.remove(ist)

    if(include is not None):
        assert type(include) is list, "include keyword argument must be a list."
        for ist in include:
            if(ist not in isotopes):
                isotopes += [ist]

    if(include_only is not None):
        assert type(include_only) is list, "include_only keyword argument must be a list."
        isotopes=include_only

    if(fLabels is not None):
        assert type(fLabels) is list, "fLabels keyword argument must be a list of strings."
        assert len(fLabels) == len(fileNames), "As many labels must be supplied as filenames."
    else:
        fLabels = [""] * len(fLabels)


    fig, ax = plt.subplots(figsize=figSize)  # Set figure size

    print("processing " + fileNames[0])
    with open(fileNames[0]) as f:
        first_data = json.load(f)

    for j, fileName in enumerate(fileNames):
        # Load data
        print("processing " + fileName)
        with open(fileName) as f:
            data = json.load(f)

        energy = []
        ratio_d = collections.defaultdict(list)
        ratio_error_d = collections.defaultdict(list)


        for ist in isotopes:
            norm_first_n = {}
            norm_first_n_error = {}

            for run in first_data:
                try:
                    # Get number produced in run
                    first_n = run["isotopes"][ist]["number"]

                    # Normalise to 10^11 protons
                    normalised_n = first_n * actual_protons / run["nEvents"]

                    # Error in normalized N
                    normalised_error = np.sqrt(first_n) * actual_protons / run["nEvents"]

                    if normalised_n > 0:
                        norm_first_n[run["energy"]] = normalised_n
                        norm_first_n_error[run["energy"]] = normalised_error

                except KeyError:
                    # None of this isotope created by first file, don't plot
                    continue


            for run in data[1:]:
                energy.append(1e3 * run["energy"])

                try:
                    # Get number produced in run
                    n = run["isotopes"][ist]["number"]

                    # Normalise to 10^11 protons
                    normalised_n = n * actual_protons / run["nEvents"]

                    # Error in normalized N
                    normalised_error = np.sqrt(n) * actual_protons / run["nEvents"]

                    # Ratio
                    ratio       = normalised_n / norm_first_n[run["energy"]]
                    ratio_error = np.sqrt( (normalised_error/normalised_n)**2 +
                        (norm_first_n_error[run["energy"]]/norm_first_n[run["energy"]])**2 )

                    if ratio==0:
                        # None of this isotope created during this run, don't plot
                        ratio = float("nan")
                        ratio_error =  float("nan")

                except ZeroDivisionError:
                    # None of this isotope created by first file, don't plot
                    ratio = float("nan")
                    ratio_error = float("nan")

                except KeyError:
                    # None of this isotope created by first file, don't plot
                    ratio = float("nan")
                    ratio_error = float("nan")


                # Append to lists
                ratio_d[ist].append(ratio)
                ratio_error_d[ist].append(ratio_error)

        # print(ratio_d)


        # Make y axis logarithmic
        if log:
            ax.set_yscale("log", nonposy='clip')

        if loglog:
            ax.set_xscale("log", nonposx='clip')
        else:
            # Set horizontal ticks to 10 MeV
            ax.set_xticks(np.arange(10,260,10))

        # Set title and axis labels
        ax.set_title(title)
        ax.set_ylabel("Ratio of isotope production to " + fLabels[0])
        ax.set_xlabel("Energy (MeV)")

        # Set limits
        ax.set_xlim(xlim)
        ax.set_ylim(ymin=ymin, ymax=ymax)

        if fileName != fileNames[0]:
            for ist in isotopes:
                # Sort according to Energy and remove NaN elements
                if not np.all(np.isnan(ratio_d[ist])):
                    x, y, e = zip(*sorted([(ix, iy, ie) for ix, iy, ie in zip(energy, ratio_d[ist], ratio_error_d[ist]) if not np.isnan(iy)]))

                    # Generate the label
                    flabel = fLabels[j]
                    if not noIstLabels:
                        flabel += " " + format_isotope(ist)

                    # Plot it
                    plt.plot(x, y, label=flabel)
                    plt.errorbar(x, y, yerr=e, fmt=' ', c='k', capsize=4, linewidth=1)

        else:
            x = [0,250]
            plt.plot(x, [1,1], label=fLabels[0], c='k', linewidth=1)

    # Place legend in best place in bottom right quadrant
    # ax.grid(which='both', linewidth=0.7)
    # ax.grid(which='major', axis='y', linewidth=0.7, c='k')

    plt.legend(bbox_to_anchor=bbox, loc='best')

    plt.savefig(outDir + outName)


# Main
"""
ratio_plot(
    fileNames=["water_HADROTHE.json"],
    fLabels=["Fluka hadrotherapy"],
    exclude=["F18", "F17", "Be11"],
    outName="water_ratio.pdf",
    title="",
    figSize=(8,4),
    noIstLabels=True,
    log=False
)
"""

ratio_plot(
    fileNames=["water_HADROTHE.json", "water_BIC.json", "water_BERT.json", ],
    fLabels=["Fluka hadrotherapy", "Geant4 Binary cascade", "Geant4 Bertini cascade"],
    include_only=["C11", "Be7", "C10"],
    outName="water_ratio.pdf",
    title="",
    ymin=0,
    ymax=2.5,
    figSize=(12,6),
    xlim=(40,250),
    log=False
)


ratio_plot(
    fileNames=["rangeshifter_t2_HADROTHE.json", "rangeshifter_t2_BIC.json", "rangeshifter_t2_BERT.json", "rangeshifter_t2_PRECISO.json"],
    fLabels=["Fluka hadrotherapy", "Geant4 Binary cascade", "Geant4 Bertini cascade", "Fluka Precision"],
    outName="rangeshifter_ratio.pdf",
    title="",
    figSize=(8,4),
    log=False
)
