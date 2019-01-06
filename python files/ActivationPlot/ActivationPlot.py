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
    fileName,
    outName,
    outDir="pdfs/",
    title="",
    xlim=(70,250),
    ymin=1,
    ymax=1e7,
    exclude=None,
    include=None,
    include_only=None,
    loglog=False,
    bbox=(0.5, 0., 0.5, 0.5)):
    # Load data
    print("processing " + fileName)
    with open(fileName) as f:
        data = json.load(f)

    # Uncomment to care about all isotopes
    """
    for run in data:
        for ist in run["isotopes"].keys():
            if ist not in isotopes_we_care_about:
                isotopes_we_care_about.append(ist)
    """

    energy = []
    act = collections.defaultdict(list)
    act_error = collections.defaultdict(list)

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


    for run in data:
        energy.append(1e3 * run["energy"])
        for ist in isotopes:
            try:
                # Get number produced in run
                n = run["isotopes"][ist]["number"]
                if n == 0:
                    raise KeyError

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

    fig, ax = plt.subplots(figsize=(10.5, 14.85))  # Make figure half a4 size

    # Make y axis logarithmic
    ax.set_yscale("log", nonposy='clip')

    if loglog:
        ax.set_xscale("log", nonposx='clip')
    else:
        # Set horizontal ticks to 10 MeV
        ax.set_xticks(np.arange(0,260,10))

    # Set title and axis labels
    ax.set_title(title)
    ax.set_ylabel("Induced activity per 100 Giga protons (Bq)")
    ax.set_xlabel("Mean energy of proton beam (MeV)")

    # Set limits
    ax.set_xlim(xlim)
    ax.set_ylim(ymin=ymin, ymax=ymax)

    for ist in isotopes:
        # Sort according to Energy and remove NaN elements
        if not np.all(np.isnan(act[ist])):
            x, y, e = zip(*sorted([(ix, iy, ie) for ix, iy, ie in zip(energy, act[ist], act_error[ist]) if not np.isnan(iy)]))

            # Plot it
            plt.plot(x, y, label=format_isotope(ist), zorder=1)
            plt.errorbar(x, y, yerr=e, fmt=' ', c='k', capsize=4, elinewidth=1, zorder=10)

    # Place legend in best place in bottom right quadrant
    ax.grid(which='both', linewidth=0.7)
    ax.grid(which='major', axis='y', linewidth=0.7, c='k')

    plt.legend(bbox_to_anchor=bbox, loc='best')

    # Remove margins
    plt.savefig(outDir + outName, bbox_inches = 'tight', pad_inches = 0)


# Main

make_plot(
    fileName="rangeshifter_t1_BIC.json",
#    title="Activation of 1cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t1_BIC.pdf",
    ymax=2e6
)

make_plot(
    fileName="rangeshifter_t2_BIC.json",
#    title="Activation of 2cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t2_BIC.pdf",
    ymax=2e6
)

make_plot(
    fileName="rangeshifter_t3_BIC.json",
#    title="Activation of 3cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t3_BIC.pdf",
    ymax=2e6
)

make_plot(
    fileName="rangeshifter_t5_BIC.json",
#    title="Activation of 5cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t5_BIC.pdf",
    ymax=2e6
)


make_plot(
    fileName="rangeshifter_t1_BERT.json",
#    title="Activation of 1cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t1_BERT.pdf",
    ymax=2e6
)


make_plot(
    fileName="rangeshifter_t2_BERT.json",
#    title="Activation of 2cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t2_BERT.pdf",
    ymax=2e6
)

make_plot(
    fileName="rangeshifter_t3_BERT.json",
#    title="Activation of 3cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t3_BERT.pdf",
    ymax=2e6
)

make_plot(
    fileName="rangeshifter_t5_BERT.json",
#    title="Activation of 5cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t5_BERT.pdf",
    ymax=2e6
)


make_plot(
    fileName="water_BIC.json",
#    title="Activation of water phantom immediately after beam turned off",
    outName="water_BIC.pdf",
    # exclude=["Be11"],
    ymin=10,
    ymax=4e7,
    bbox=(0.75, 0., 0.25, 0.4),
    xlim=(20,250),
    # loglog=True
)


make_plot(
    fileName="water_BERT.json",
#    title="Activation of water phantom immediately after beam turned off",
    outName="water_BERT.pdf",
    ymin=10,
    ymax=4e7,
    xlim=(20,250)
)

make_plot(
    fileName="water_HADROTHE.json",
#    title="Activation of water phantom immediately after beam turned off",
    outName="water_HADROTHE.pdf",
    ymin=10,
    ymax=4e7,
    bbox=(0.75, 0., 0.25, 0.4),
    xlim=(20,250)
)

make_plot(
    fileName="rangeshifter_t1_HADROTHE.json",
#    title="Activation of 1cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t1_HADROTHE.pdf",
    exclude = ["F17", "C15"],
    ymin=0.1,
    ymax=2e6
)

make_plot(
    fileName="rangeshifter_t2_HADROTHE.json",
#    title="Activation of 2cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t2_HADROTHE.pdf",
    exclude = ["F17", "C15"],
    ymin=0.1,
    ymax=2e6
)

make_plot(
    fileName="rangeshifter_t3_HADROTHE.json",
#    title="Activation of 3cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t3_HADROTHE.pdf",
    exclude = ["F17", "C15"],
    ymin=0.1,
    ymax=2e6
)

make_plot(
    fileName="rangeshifter_t5_HADROTHE.json",
#    title="Activation of 5cm thick range shifter immediately after beam turned off",
    outName="rangeshifter_t5_HADROTHE.pdf",
    exclude = ["F17", "C15"],
    ymin=0.1,
    ymax=2e6
)

make_plot(
    fileName="rangeshifter_t1_PRECISO.json",
    outName="rangeshifter_t1_PRECISIO.pdf",
    exclude = ["F17", "C15"],
    ymin=0.1,
    ymax=2e6
)
