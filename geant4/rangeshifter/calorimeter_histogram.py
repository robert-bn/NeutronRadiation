#!/usr/bin/env python
"""This Python script displays histogram as saved in 4c in CSV format.

How to run it:
  - python calorimeter_histogram.py
  - python calorimeter_histogram.py name_of_a_file.csv

If your data is written into task4_h1_eDep.csv, your don't have to
specify the file name as argument.

Note: It does not open any other Geant4 output files.
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import codecs
import numpy as np
import sys
import os


def load_csv(path):
    """Load a histogram as output from Geant4 analysis tools in CSV format.
    
    Note: This method is useful for ANY Geant4 analysis tools histogram.

    Parameters
    ----------
    path: str
        Path to the CSV file
    """
    meta = {}
    data = []
    with codecs.open(path, encoding="ASCII") as in_file:
        for line in in_file:
            if line.startswith("#"):
                try:
                    key, value = line[1:].strip().split(" ", 1)
                    meta[key] = value   # TODO: There are duplicit entries :-()
                except:
                    pass
            else:
                try:
                    data.append([float(frag) for frag in line.split(",")])
                except:
                    pass
    if "class" not in meta or (meta["class"] != "tools::histo::h1d"):
        raise RuntimeError("The file {0} is not an CSV export of a Geant4 histogram.".format(path))
    data = np.asarray(data)
    return data, meta


def plot_histogram(path):
    """Plot the calorimeter histogram and saves it to histogram.png.
    
    Note: This method works only with the calorimeter histogram from task 4c.
    
    Parameters
    ----------
    path: str
        The path to the file.
    """
    try:
        import seaborn as sns
    except:
        pass
    if not os.path.isfile(path):
        print("File {0} does not exist. Make sure you created it.".format(path))
        return
    data, meta = load_csv(path)
    fig, ax = plt.subplots()
    if data[1,0] > 0:
        data[:,1] /= (data[1,0] * 1000.0)
    nbin, minbin, maxbin = (int(z) for z in meta["axis"].split(" ")[1:])
    x = np.linspace(minbin, maxbin, nbin + 1)
    bin_width = (maxbin - minbin) / (nbin * 1.0)
    
    # Alternating red and green bins.
    ax.bar(x[:-1:2], data[1:-1:2,1], bin_width, color="red", label="absorber")
    ax.bar(x[1:-1:2], data[2:-1:2,1], bin_width, color="green", label="scintillator")
    ax.set_xlim(minbin, maxbin)
    ax.legend()
    ax.set_title(meta["title"])
    ax.set_xlabel("x [cm]")
    ax.set_ylabel("deposited energy [MeV]")
    plt.show()
    fig.savefig("histogram.png")
    print("Histogram has been saved to histogram.png")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        path = sys.argv[1]
    else:
        path = "task4_h1_eDep.csv"
    plot_histogram(path)
