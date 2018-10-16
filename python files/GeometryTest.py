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
        # print("processing {}".format(filename))
        detector_dfs.append(pd.read_csv(directory + filename, sep=' ', comment='#', header=None, names=f_header))
        # throw away non-neutrons
        detector_dfs[-1] = detector_dfs[-1].loc[detector_dfs[-1]['PDGid'] == NEUTRON_PDGid]
        nn.append(len(detector_dfs[-1]))
        z.append(detector_dfs[-1].z.mean())

data = pd.DataFrame({'nn':nn, 'z':z, 'error':np.sqrt(nn)}).sort_values('z')

# normalise to first element
normalization = data['nn'].max()
data['nn'] = data['nn']/normalization
data['error'] = data['error']/normalization
keys = data['z'] > 490


pdata = data.as_matrix(['z', 'nn', 'error'])

fit = np.polyfit(pdata[6:,0],pdata[6:,1],1,w=1/pdata[6:,2])  # don't include first 6 points in regression
fit_fn = np.poly1d(fit)

plt.errorbar(pdata[:,0], pdata[:,1], pdata[:,2], fmt=" o ", capsize=3, markersize=2)
plt.plot(pdata[6:,0], fit_fn(pdata[6:,0]), '--k')
print(np.sum((fit_fn(pdata[6:,0])-pdata[6:,1])**2/pdata[6:,2]**2))
print(fit)
plt.show()
