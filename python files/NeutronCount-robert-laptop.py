# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import pandas as pd
import os

NEURTRON_PDGid = 2112

directory = "../data/NeutronCount/"
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

detector_dfs = []
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        detector_dfs.append(pd.read_csv(directory + filename, sep=' ', comment='#', header=None, names=f_header))


n_neutrons = 0
n_protons = 100000
100000
for df in detector_dfs:
    n_neutrons+=df.loc["PDGid" == NEURTRON_PDGid].count()[0]

print(n_neutrons)
print(n_protons)
print(n_neutrons/n_protons)
