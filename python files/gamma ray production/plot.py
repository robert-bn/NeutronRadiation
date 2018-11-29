import numpy as np
import matplotlib.pyplot as plt
import json

# Load data
with open("isotopes.json") as f:
    data = json.load(f)

with open("saturation.json") as f:
    act_data = json.load(f)


# Function definitions
def plot_activity(activity, tmin=0, tmax=3600, n=1000, ax=None, title=None, labels=True, legend=True):
    # Plot activity vs time
    if ax is None:
        fig, ax = plt.subplots()

    t = np.linspace(tmin,tmax,n)

    for ist in data.keys():
        ax.plot(
            t,
            activity[ist] * np.exp(-np.log(2)/data[ist]['halfLife']*t),
            label="$^{{{A}}}${elm}".format(A=data[ist]['A'], elm=data[ist]['symbol'])
        )

    ax.set_xlim(tmin,tmax)

    if title is None:
        ax.set_title("Activity vs time since beam turned off")
    elif type(title) is str:
        ax.set_title(title)

    if labels:
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Activity (Bq)")

    if legend:
        ax.legend()

    if ax is None:
        plt.show()


def plot_gamma(activity, tmin=0, tmax=3600, n=1000, ax=None, title=None, labels=True, legend=True):
    # Plot gamma rate vs time
    if ax is None:
        fig, ax = plt.subplots()

    t = np.linspace(tmin,tmax,n)

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

    ax.set_xlim(tmin,tmax)

    if title is None:
        ax.set_title("Gamma ray emission vs time since beam turned off")
    elif type(title) is str:
        ax.set_title(title)

    if labels:
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Activity (Bq)")

    if legend:
        ax.legend()

    if ax is None:
        plt.show()


def plot_beta(activity, tmin=0, tmax=3600, n=1000, ax=None, title=None, labels=True, legend=True):
    # Plot activity vs time
    if ax is None:
        fig, ax = plt.subplots()

    t = np.linspace(tmin,tmax,n)

    y = []
    label = []

    for ist in data.keys():
        for gamma in data[ist]["gamma"]:
            if gamma["type"] == "beta+":
                y.append(gamma["branchingRatio"] * gamma["multiplicity"] * activity[ist] * np.exp(-np.log(2)/data[ist]['halfLife']*t))
                label.append("$^{{{A}}}${elm}".format(
                        A=data[ist]['A'],
                        elm=data[ist]['symbol']
                    )
                )

    ax.stackplot(t, y, labels=label)
    ax.set_xlim(tmin,tmax)

    if legend:
        ax.legend()

    if labels:
        ax.set_xlabel("Time (seconds)")
        ax.set_ylabel("Activity (Bq)")

    if title is None:
        ax.set_title("$\\beta⁺$ emission rate against time since beam turned off")
    elif type(title) is str:
        ax.set_title(title)

    if ax is None:
        plt.show()


# Main

# Plot each graph for 200 MeV, 230 MeV for 2cm thickness
fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True)

plot_activity(act_data[0]["activation"], ax=axes[0,0], labels=False)
plot_gamma(   act_data[0]["activation"], ax=axes[0,1], labels=False)
plot_beta(    act_data[0]["activation"], ax=axes[0,2], labels=False)
plot_activity(act_data[1]["activation"], ax=axes[1,0], title=False)
plot_gamma(   act_data[1]["activation"], ax=axes[1,1], title=False)
plot_beta(    act_data[1]["activation"], ax=axes[1,2], title=False)

plt.show()
