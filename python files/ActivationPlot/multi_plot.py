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


actual_protons = 1e11
isotopes_we_care_about = ["Be7", "C10", "C11", "O15", "O14", "N13", "N16", "F17", "F18", "Be11", "N17", "C15"]


def make_plot(
    title,
    outName,
    fileName=None,
    ymin=1,
    ymax=1e7,
    fileList=None,
    labels=None,
    exclude=None,
    include=None,
    include_only=None,
    loglog=False,
    error=True,
    bbox=(0.5, 0., 0.5, 0.5)):

    # Uncomment to care about all isotopes
    """
    for run in data:
        for ist in run["isotopes"].keys():
            if ist not in isotopes_we_care_about:
                isotopes_we_care_about.append(ist)
    """


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



    fig, ax = plt.subplots(figsize=(10.5, 14.85))  # Make figure half a4 size

    # Make y axis logarithmic
    ax.set_yscale("log", nonposy='clip')

    if loglog:
        ax.set_xscale("log", nonposx='clip')
    else:
        # Set horizontal ticks to 10 MeV
        ax.set_xticks(np.arange(70,260,10))

    # Set title and axis labels
    ax.set_title(title)
    ax.set_ylabel("Induced activity per 100 Giga protons (Bq)")
    ax.set_xlabel("Energy (MeV)")

    # Set limits
    ax.set_xlim((70,250))
    ax.set_ylim(ymin=ymin, ymax=ymax)

    if fileList is None:
        fileList = [fileName,]

    ist_colors= {}

    # Load data
    for i, fn in enumerate(fileList):
        energy = []
        act = collections.defaultdict(list)
        act_error = collections.defaultdict(list)

        print("processing " + fn)
        with open(fn) as f:
            data = json.load(f)


        for run in data:
            energy.append(1e3 * run["energy"])
            for ist in isotopes:
                try:

                    # Get number produced in run
                    n = run["isotopes"][ist]["number"]

                    # Normalise to 10^11 protons
                    normalised_n = n * actual_protons / run["nEvents"]

                    # Error in normalized N
                    normalised_error = np.sqrt(n) * actual_protons / run["nEvents"]

                    # Get saturation activity & error
                    r_act, r_act_error = saturation(
                        n=normalised_n,
                        error=normalised_error,
                        lifeTime=run["isotopes"][ist]["lifeTime"]
                    )
                except KeyError:
                    # None of this isotope created during this run, don't plot
                    r_act = float("nan");
                    r_act_error = float("nan");

                # Append to lists
                act[ist].append(r_act)
                act_error[ist].append(r_act_error)

        for ist in isotopes:
            # Sort according to Energy and remove NaN elements
            if not np.all(np.isnan(act[ist])):
                x, y, e = zip(*sorted([(ix, iy, ie) for ix, iy, ie in zip(energy, act[ist], act_error[ist]) if not np.isnan(iy)]))

                # Plot it
                if ist in ist_colors:
                    c = ist_colors[ist]
                    if labels is not None:
                        p = plt.plot(x, y, color=c, label=labels[i] + " - " + format_isotope(ist), zorder=1)
                    else:
                        p = plt.plot(x, y, color=c, label=format_isotope(ist), zorder=1)

                else:
                    if labels is not None:
                        p = plt.plot(x, y, label=labels[i] + " - " + format_isotope(ist), zorder=1)
                    else:
                        p = plt.plot(x, y, label=format_isotope(ist), zorder=1)
                    ist_colors[ist] = p[0].get_color()
                if error[i]:
                    plt.errorbar(x, y, yerr=e, fmt=' o ', c='k', capsize=4, markersize=2, zorder=2)
                else:
                    plt.scatter(x, y, marker='x', c='k', s=4, zorder=2)

    # Place legend in best place in bottom right quadrant
    ax.grid(which='both', linewidth=0.7)
    ax.grid(which='major', axis='y', linewidth=0.7, c='k')

    plt.legend(bbox_to_anchor=bbox, loc='best')

    plt.savefig(outName)


# Main
"""
make_plot(
    fileName="output_t1.json",
    title="Activation of 1cm thick range shifter immediately after beam turned off",
    outName="1cm-rangeshifter.svg",
    ymax=2e6
)

make_plot(
    fileName="output_t2.json",
    title="Activation of 2cm thick range shifter immediately after beam turned off",
    outName="2cm-rangeshifter.svg",
    ymax=2e6
)

make_plot(
    fileName="output_t3.json",
    title="Activation of 3cm thick range shifter immediately after beam turned off",
    outName="3cm-rangeshifter.svg",
    ymax=2e6
)

make_plot(
    fileName="output_t5.json",
    title="Activation of 5cm thick range shifter immediately after beam turned off",
    outName="5cm-rangeshifter.svg",
    ymax=2e6
)


make_plot(
    fileName="water.json",
    title="Activation of water phantom immediately after beam turned off",
    outName="water.svg",
    # exclude=["Be11"],
    ymin=10,
    ymax=4e7,
    bbox=(0.75, 0., 0.25, 0.4),
    # loglog=True
)


make_plot(
    fileName="water_BERT.json",
    title="Activation of water phantom immediately after beam turned off",
    outName="water-BERT.svg",
    ymin=10,
    ymax=4e7
)
"""

make_plot(
    fileList=["theoretical.json", "output_t1.json"],
    labels=["Theoretical", "Geant4 binary cascade"],
    title="Activation of 1 cm range shifter immediately after beam turned off",
    outName="theoretical.svg",
    error=[False, True],
    marker=['x', ' o ']
    ymax=2e6,
    include_only=['Be7', 'C10', 'C11', 'O14', 'O15']
)
