# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import pandas as pd
import os

NEURTRON_PDGid = 2112
PROTON_PDGid = 2212
GAMMA_PDGid = 22

directory = "./data/WaterActivation/"
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

detector_dfs = []
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        detector_dfs.append(pd.read_csv(directory + filename, sep=' ', comment='#', header=None, names=f_header))

n_neutrons = 0
n_input = 100000
n_protons = 0
n_gamma = 0

for df in detector_dfs:
    n_neutrons+=len(df.loc[df["PDGid"] == NEURTRON_PDGid])
    n_protons+=len(df.loc[df["PDGid"] == PROTON_PDGid])
    n_gamma+=len(df.loc[df["PDGid"] == GAMMA_PDGid])

print(n_neutrons)
print(n_protons)
print(n_gamma)
