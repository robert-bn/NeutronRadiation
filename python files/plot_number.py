# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

PROTON_PIGUID = 2212
filename = "Det.txt"
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

my_data = pd.read_csv(filename, sep=' ', comment='#', header=None, names=f_header)
my_data = my_data.loc[(my_data['PDGid'] == PROTON_PIGUID) & (my_data['Pz'] > 0)]                      # throw away non-protons
detector_z = sorted(my_data.z.unique())                                         # return all unique z values, each corrosponding to a particular detector
print(detector_z)
number = np.empty_like(detector_z)

for i, z in enumerate(detector_z):
    specific_detector = my_data.loc[my_data['z'] == z] # selects only rows with same z
    number[i] = specific_detector.count()[0]
    print("Loading Detector {n} of {tot_n}. Number of events = {n_events}".format(n=i, tot_n=len(detector_z), n_events=number[i]))

plt.plot(detector_z, number)
plt.show()
