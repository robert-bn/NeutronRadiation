# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import pandas as pd
import numpy as np
import os

NEURTRON_PDGid = 2112

# directory = "../data/NeutronStoppage/"
directory = "../g4beamline files/Neutron Detector Water/"
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]


dfs = []
input_dfs = []

for filename in os.listdir(directory):
    if filename.endswith(".txt") and not filename.startswith("Input"):
        print(filename)
        print("Input" + filename)
        # dfs.append(pd.read_csv(directory + filename, sep=' ', comment='#', header=None, names=f_header))
        # input_dfs.append(pd.read_csv(directory + "Input" + filename, sep=' ', comment='#', header=None, names=f_header))

n = []

for i in range(len(input_dfs)):
    input_dfs[i] = input_dfs[i].loc[input_dfs[i]['Pz'] > 0] # throw away backscattered neutrons
    dfs[i] = dfs[i].loc[dfs[i]['PDGid'] == NEURTRON_PDGid]  # throw away non-neutrons
    n.append(len(input_df[i]))
    print(len(n[i]))
    print(len(dfs[i])/len(n[i]),end='')
    print(" +/- ", end='')
    print(1/np.sqrt(n[i]))



df = pd.read_csv(directory + "Det.txt", sep=' ', comment='#', header=None, names=f_header)

input_df = input_df.loc[input_df['Pz'] > 0]
df = df.loc[df['PDGid'] == 2112]

print(len(input_df))
print(len(df)/len(input_df),end='')
print(" +/- ", end='')
print(1/np.sqrt(len(input_df)))

"""
n_neutrons = df
# import the module
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

directory = "../data/"
filename = "NeutronStoppageConcrete.txt"

#x y z Px Py Pz t PDGid EventID TrackID ParentID Weight Bx By Bz Ex Ey Ez ProperTime PathLength PolX PolY PolZ InitX InitY InitZ InitT InitKE
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight", "Bx", "By", "Bz", "Ex", "Ey", "Ez", "ProperTime", "PathLength", "PolX", "PolY", "PolZ", "InitX", "InitY", "InitZ", "InitT", "InitKE"]
df = pd.read_csv("Det.txt", comment='#', sep=' ', header=None, names=f_header)
# open the file

A = (np.sqrt((df[['Px', 'Py', 'Pz']] ** 2 ).sum(axis=1))).mean()
print(A)


#for entry in df['Px']:
#    print(entry)
"""
