import numpy as np
import matplotlib.pyplot as plt
import json

directory = "data/"
# Load data
with open(directory + "isotopes.json") as f:
    data = json.load(f)

with open(directory + "saturation(FLUKA).json") as f:
    act_data = json.load(f)


# Function definitions
def plot_activity(activity, tmin=0, tmax=3600, n=1000, ax=None, title=None, xlabel=True, ylabel=True, legend=True, grid=True):
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
    ax.set_ylim(bottom=0)

    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    if grid:
        ax.grid(True)

    if title is None:
        ax.set_title("Activity vs time since beam turned off")
    elif type(title) is str:
        ax.set_title(title)

    if xlabel:
        ax.set_xlabel("Time (seconds)")
    if ylabel:
        ax.set_ylabel("Activity (Bq)")

    if legend:
        ax.legend()

    if ax is None:
        plt.show()


def plot_gamma(activity, tmin=0, tmax=3600, n=1000, ax=None, title=None, xlabel=True, ylabel=True, legend=True, grid=True):
    # Plot gamma rate vs time
    if ax is None:
        fig, ax = plt.subplots()

    t = np.linspace(tmin,tmax,n)

    for ist in data.keys():
        for gamma in data[ist]["gamma"]:
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
    ax.set_ylim(bottom=0)

    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    if grid:
        ax.grid(True)

    if title is None:
        ax.set_title("Gamma ray emission vs time since beam turned off")
    elif type(title) is str:
        ax.set_title(title)

    if xlabel:
        ax.set_xlabel("Time (seconds)")
    if ylabel:
        ax.set_ylabel("Activity (Bq)")

    if legend:
        ax.legend()

    if ax is None:
        plt.show()


def plot_beta(activity, tmin=0, tmax=3600, n=1000, ax=None, title=None, xlabel=True, ylabel=True, legend=True, grid=True):
    # Plot activity vs time
    if ax is None:
        fig, ax = plt.subplots()

    t = np.linspace(tmin,tmax,n)

    y = []
    label = []

    for ist in data.keys():
        for gamma in data[ist]["gamma"]:
            y.append(gamma["branchingRatio"] * gamma["multiplicity"] * activity[ist] * np.exp(-np.log(2)/data[ist]['halfLife']*t))
            label.append("$^{{{A}}}${elm}".format(
                    A=data[ist]['A'],
                    elm=data[ist]['symbol']
                )
            )

    if grid:
        ax.grid(True, zorder=0)

    ax.stackplot(t, y, labels=label, zorder=3)
    ax.set_xlim(tmin,tmax)
    ax.set_ylim(bottom=0)

    ax.ticklabel_format(style='sci', axis='y', scilimits=(0,0))

    if legend:
        ax.legend()

    if xlabel:
        ax.set_xlabel("Time (seconds)")
    if ylabel:
        ax.set_ylabel("Activity (Bq)")

    if title is None:
        ax.set_title("$\\beta⁺$ emission rate against time since beam turned off")
    elif type(title) is str:
        ax.set_title(title)

    if ax is None:
        plt.show()


def act(activity, t, ist, gamma):
    # Plot gamma rate vs time
    return gamma["branchingRatio"] * gamma["multiplicity"] * activity[ist] * np.exp(-np.log(2)/data[ist]['halfLife']*t)

def activityTOM(activity):
    TOM = [60,120,300]
    activities = []
    efficiency = []
    print(activities)
    for ist in data.keys():
        for i in range(len(TOM)):
            for gamma in data[ist]["gamma"]:

                activities.append(gamma["branchingRatio"] * gamma["multiplicity"] * activity[ist] * np.exp(-np.log(2)/data[ist]['halfLife']*TOM[i]))
                efficiency.append(1/(((gamma["energy"]*0.001) + 1)**3))
                print(activities[i])
    print(activities)
    #print(efficiency)

def nice_table(filename, activity):
    TOM = [60,120,300]
    with open(filename, 'w') as f:
        f.write("{c1},{c2},{c3},{c4},{c5}\n".format(
                        c1="Photopeak",
                        c2="Energy",
                        c3="Activity after 60s",
                        c4="Activity after 120s",
                        c5="Activity after 300s",
                    ))
        for ist in data.keys():
            for gamma in data[ist]["gamma"]:
                activities_60 = gamma["branchingRatio"] * gamma["multiplicity"] * activity[ist] * np.exp(-np.log(2)/data[ist]['halfLife']*TOM[0])
                activities_120 = gamma["branchingRatio"] * gamma["multiplicity"] * activity[ist] * np.exp(-np.log(2)/data[ist]['halfLife']*TOM[1])
                activities_300 = gamma["branchingRatio"] * gamma["multiplicity"] * activity[ist] * np.exp(-np.log(2)/data[ist]['halfLife']*TOM[2])
                f.write("{c1},{c2},{c3},{c4},{c5}\n".format(
                    c1= ist,
                    c2=gamma["energy"],
                    c3=activities_60,
                    c4=activities_120,
                    c5=activities_300
                ))


# Main

nice_table("GammaTables.csv",act_data[0]["activation"])

'''
# pad title
plt.rcParams['axes.titlepad'] = 20

# Plot each graph for 200 MeV, 230 MeV for 2cm thickness
fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, figsize=(18,10))

plot_activity(act_data[0]["activation"], ax=axes[0,0], xlabel=False)
plot_gamma(   act_data[0]["activation"], ax=axes[0,1], xlabel=False)
plot_beta(    act_data[0]["activation"], ax=axes[0,2], xlabel=False)
plot_activity(act_data[1]["activation"], ax=axes[1,0], title=False)
plot_gamma(   act_data[1]["activation"], ax=axes[1,1], title=False)
plot_beta(    act_data[1]["activation"], ax=axes[1,2], title=False)

# remove verticle space between subplots
plt.subplots_adjust(hspace=.0)
plt.subplots_adjust(wspace=.2)

plt.show()
# save plot
# plt.savefig("test.pdf", papertype='a3', dpi=100)
'''
