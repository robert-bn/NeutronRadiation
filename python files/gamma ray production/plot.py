import numpy as np
import matplotlib.pyplot as plt
import json

activity = {'Be7':1.0, 'C11':1.0, 'O14':1.0, 'O15':1.0, 'C10':1.0}

# Read in data from Json
with open("isotopes.json") as f:
    data = json.load(f)

def plot_activity():
    # Plot activity vs time
    fig, ax = plt.subplots()

    t = np.linspace(0,3600,1000)

    for ist in data.keys():
        ax.plot(
            t,
            activity[ist] * np.exp(-np.log(2)/data[ist]['halfLife']*t),
            label="$^{{{A}}}${elm}".format(A=data[ist]['A'], elm=data[ist]['symbol'])
        )

    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Activity (Bq)")
    ax.legend()
    plt.show()


def plot_gamma():
    # Plot gamma rate vs time
    fig, ax = plt.subplots()

    t = np.linspace(0,3600,10000)

    for ist in data.keys():
        for gamma in data[ist]["gamma"]:
            print(gamma["branchingRatio"])
            print(gamma["multiplicity"])
            print(activity[ist])
            np.exp(-np.log(2)/data[ist]['halfLife']*t),
            ax.plot(
                t,
                gamma["branchingRatio"] * gamma["multiplicity"] * activity[ist] * np.exp(-np.log(2)/data[ist]['halfLife']*t),
                label="$^{{{A}}}${elm} - {eng} keV photopeak".format(
                    A=data[ist]['A'],
                    elm=data[ist]['symbol'],
                    eng= gamma["energy"]
                )
            )

    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Activity (Bq)")
    ax.legend()
    plt.show()


# Main
plot_gamma()
