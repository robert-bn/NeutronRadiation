# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

NEUTRON_PDGid = 2112

directory = "../g4beamline files/GeometryTest/"
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

detector_dfs = []
nn = []
z = []

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".txt") and filename.startswith("Det"):
        print("processing {}".format(filename))
        detector_dfs.append(pd.read_csv(directory + filename, sep=' ', comment='#', header=None, names=f_header))
        detector_dfs[-1] = detector_dfs[-1].loc[detector_dfs[-1]['PDGid'] == NEUTRON_PDGid] 
        nn.append(len(detector_dfs[-1]))
        z.append(detector_dfs[-1].z.mean())

nn = np.array(nn)
z = np.array(z)
error = np.sqrt(nn)

# normalise to first element
minidx = np.argmin(z)
normalization = nn[minidx]
nn = nn/normalization
error = error/normalization

fit = np.polyfit(z,nn,1, w=1/error)
fit_fn = np.poly1d(fit)

plt.plot(z, fit_fn(z), '--k')
plt.errorbar(z, nn, error, fmt="o")
print(np.sum((fit_fn(z)-nn)**2/error**2))
print(fit)
plt.show()
