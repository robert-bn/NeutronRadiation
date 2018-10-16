# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import pandas as pd
from numpy import sqrt
import os

NEUTRON_PDGid = 2112
n_in = 1e6 * (250/1000)**2

directory = "../g4beamline files/NeutronAttenuationTest/"
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

df = pd.read_csv(directory + "Det293.txt", sep=' ', comment='#', header=None, names=f_header)

df = df.loc[df["PDGid"] == NEUTRON_PDGid] # throw away non-neutrons
print(len(df)/n_in, end='')
print("+/-", end='')
print(1/sqrt(len(df))/n_in)
