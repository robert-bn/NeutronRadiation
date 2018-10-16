# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import pandas as pd
import os

NEURTRON_PDGid = 2112

directory = "../g4beamline files/NeutronAttenuation/"
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

detector_dfs = []
input_dfs = []
n_in = []
n_out = []

# test commit

for filename in os.listdir(directory):
    if filename.endswith(".txt") and filename.startswith("Det"):
        print(filename)
        detector_dfs.append(pd.read_csv(directory + filename, sep=' ', comment='#', header=None, names=f_header))
        input_dfs.append(pd.read_csv(directory + "Input" + filename, sep=' ', comment='#', header=None, names=f_header))

for i in range(len(input_dfs)):
    input_dfs[i] = input_dfs[i].loc[input_dfs[i]['Pz'] > 0] # throws away backscattered neutrons
    n_in.append(len(input_dfs[i]))
    n_out.append(len(detector_dfs[i]))

print(n_in)

"""
for i, depth in enumerate([100,120,140,160,180,200,220,240,260,280]):
    print(i)
    print( "{}, {}, {}".format(depth, n_in[i], n_out[i]) )
"""
