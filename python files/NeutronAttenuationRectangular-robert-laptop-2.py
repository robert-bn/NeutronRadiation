# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

NEUTRON_PDGid = 2112

n_in = 1000000 * (250/700)**2

directory = "../g4beamline files/NeutronAttenuationRectangular/"
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

depth = [100,120,140,160,180,200,220,240,260,280]
detector_dfs = []
n_out = []

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".txt") and filename.startswith("Det"):
        detector_dfs.append(pd.read_csv(directory + filename, sep=' ', comment='#', header=None, names=f_header))
        detector_dfs[-1] = detector_dfs[-1].loc[detector_dfs[-1]['PDGid'] == NEUTRON_PDGid] # throw away non-neutrons
        n_out.append(len(detector_dfs[-1]))

n_out = np.array(n_out)


plt.plot(depth, np.log(n_out/n_in))
plt.errorbar(depth, np.log(n_out/n_in), 1/np.sqrt(n_out), marker='o', color='k', linestyle='')
plt.xlabel("Thickness (mm)")
plt.ylabel("Neutron Survival Fraction (Log)")
plt.title("Neutron Attenuation in concrete")
plt.show()


plt.plot(depth, n_out/n_in)
plt.errorbar(depth, n_out/n_in, np.sqrt(n_out)/n_in, marker='o', color='k', linestyle='')
plt.xlabel("Thickness (mm)")
plt.ylabel("Neutron Survival Fraction")
plt.title("Neutron Attenuation in concrete")
plt.show()

df = pd.DataFrame({'x':depth, 'survival fraction':np.log(n_out/n_in), 'error':1/np.sqrt(n_out)})
df.to_csv("../data/NeutronAttenuationRectangular.csv", sep=',', index=False, columns=['x', 'survival fraction', 'error'])
