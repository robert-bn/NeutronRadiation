# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

NEUTRON_PDGid = 2112
PROTON_PDGid = 2112
NeutronsOnly=False

n_in = 100000

if os.name == "posix":
    # linux
    directory = "../data/TeflonRangeShifter/"
elif os.name == "nt":
    # windows
    directory = "./data/TeflonRangeShifter/"

f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

depth = np.array([1,2,3])
n_out = [n_in,]

for d in depth:
    print(directory + "Base{}.txt".format(d))
    if d>0:
        dfb = pd.read_csv(directory + "Base{}.txt".format(d), sep=' ', comment='#', header=None, names=f_header)
        dfx = pd.read_csv(directory + "Wallx{}.txt".format(d), sep=' ', comment='#', header=None, names=f_header)
        dfy = pd.read_csv(directory + "Wallz{}.txt".format(d), sep=' ', comment='#', header=None, names=f_header)
        df = pd.concat([dfb, dfx, dfy])
        if NeutronsOnly==True:
            n_out.append(np.count_nonzero(df['PDGid']==NEUTRON_PDGid))
        else:
            n_out.append(df.size)


dfb = pd.read_csv(directory + "Base.txt", sep=' ', comment='#', header=None, names=f_header)
dfx = pd.read_csv(directory + "Wallx.txt", sep=' ', comment='#', header=None, names=f_header)
dfy = pd.read_csv(directory + "Wallz.txt", sep=' ', comment='#', header=None, names=f_header)
df  = pd.concat([dfb, dfx, dfy])
df  = df.loc[df['PDGid'] == PROTON_PDGid] # throw away non-protons

df['energy'] = np.sqrt((df[['Px', 'Py', 'Pz']] ** 2).sum(axis=1) + 938**2) - 938
df['energy'].hist(bins=100)
print(df.size)
plt.show()
