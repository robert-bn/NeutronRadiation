# reads in a g4beamline output TEXT file, and plots the mean energy vs distance
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

PROTON_PIGUID = 2212
filename = "Det.txt"
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

my_data = pd.read_csv(filename, sep=' ', comment='#', header=None, names=f_header)
# my_data = my_data.loc[(my_data['PDGid'] == PROTON_PIGUID) & (my_data['Pz'] > 0)] # throw away non-protons & back-scattered protons
my_data = my_data.loc[(my_data['ParentID'] == 0)] # throw away protons not from beam
detector_z = sorted(my_data.z.unique())                          # return all unique z values, each corrosponding to a particular detector
print(detector_z)
mean_energy = np.empty_like(detector_z)

for i, z in enumerate(detector_z):
    specific_detector = my_data.loc[my_data['z'] == z] # selects only rows with same z
    mean_energy[i] = (specific_detector[['Px', 'Py', 'Pz']] ** 2).sum(axis=0).sum()  /(938 * 2 * specific_detector.count()[0])
    print("Loading Detector {n} of {tot_n}. Number of events = {n_events}".format(n=i, tot_n=len(detector_z), n_events=specific_detector.count()[0]))

plt.plot(detector_z, mean_energy)
plt.show()
