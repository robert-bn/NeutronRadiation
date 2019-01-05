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
    colour=None,
    style=None,
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
            ax.set_xticks(np.arange(0,250,50))
            ax.set_xticks(np.arange(10,260,10), minor=True)

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
                    if colour is not None and style is not None:
                        plt.plot(x, y, label=flabel, c=colour[ist], ls=style[fLabels[j]])
                    else:
                        plt.plot(x, y, label=flabel)

                    plt.errorbar(x, y, yerr=e, fmt=' ', c='k', capsize=4, linewidth=0.5)

        else:
            x = [0,250]
            plt.plot(x, [1,1], c='k', linewidth=0.5)

    # Place legend in best place in bottom right quadrant
    # ax.grid(which='both', linewidth=0.7)
    # ax.grid(which='major', axis='y', linewidth=0.7, c='k')

    plt.legend(bbox_to_anchor=bbox, loc='best')

    plt.savefig(outDir + outName, bbox_inches = 'tight', pad_inches = 0)



# Main
technicolor = {"C11":"r", "O14":"b", "O15":"g", "N16":"orange", "N13":"magenta"}
finestyle = {"Binary cascade":"--", "Bertini cascade":"-"}

ratio_plot(
    fileNames=["water_HADROTHE.json", "water_BIC.json", "water_BERT.json", ],
    fLabels=["Fluka hadrotherapy", "Binary cascade", "Bertini cascade"],
    style=finestyle,
    colour=technicolor,
    include_only=["C11", "O15", "N13"],
    outName="water_C11_O15_ratio.pdf",
    title="",
    ymax=3,
    figSize=(4,6),
    xlim=(40,250),
    log=False
)

ratio_plot(
    fileNames=["water_HADROTHE.json", "water_BIC.json", "water_BERT.json", ],
    fLabels=["Fluka hadrotherapy", "Binary cascade", "Bertini cascade"],
    style=finestyle,
    colour=technicolor,
    include_only=["O14", "N16"],
    outName="water_O14_ratio.pdf",
    title="",
    ymin=0,
    ymax=10,
    figSize=(4,6),
    xlim=(40,250),
    log=False
)
