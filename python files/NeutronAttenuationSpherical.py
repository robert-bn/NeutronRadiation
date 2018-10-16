# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

NEUTRON_PDGid = 2112

n_in = 100000

directory = "../data/NeutronAttenuationSpherical/"
f_header = ["x", "y", "z", "Px", "Py", "Pz", "t", "PDGid", "EventID", "TrackID", "ParentID", "Weight"]

depth = np.arange(0,300,10)
n_out = [n_in,]
n_out_neutrons = [n_in,]


for d in depth:
    # print(directory + "Base{}.txt".format(d))
    if d>0:
        dfb = pd.read_csv(directory + "Base{}.txt".format(d), sep=' ', comment='#', header=None, names=f_header)
        dfx = pd.read_csv(directory + "Wallx{}.txt".format(d), sep=' ', comment='#', header=None, names=f_header)
        dfy = pd.read_csv(directory + "Wallz{}.txt".format(d), sep=' ', comment='#', header=None, names=f_header)
        df = pd.concat([dfb, dfx, dfy])
        n_out.append(len(df))
        n_out_neutrons.append(np.sum(df['PDGid']==NEUTRON_PDGid))

n_out = np.array(n_out)
n_out_neutrons = np.array(n_out_neutrons)
y_n = n_out_neutrons/n_in
y = n_out/n_in
y_log = np.log(n_out/n_in)
y_log_error = 1/np.sqrt(n_out)

f_idx = 15 # first index to calculate regression from

fit = np.polyfit(depth[f_idx:],y_log[f_idx:],1,w=1/y_log_error[f_idx:]**2)  # don't include first 6 points in regression
fit_fn = np.poly1d(fit)

chi2 = np.sum( (y_log[f_idx:] - fit_fn(depth[f_idx:])) ** 2 / y_log_error[f_idx:]**2)
red_chi2 = chi2/(len(depth) - f_idx - 2)
print("fitting parameters: {}".format(fit))
print("chi^2: {}".format(chi2))
print("reduced chi^2: {}".format(red_chi2))

print("half value layer: {} mm".format(-np.log(2)/fit[0]))
print("tenth value layer: {} mm".format(-np.log(10)/fit[0]))
# plot data
# plt.plot(depth, np.log(y))

plt.errorbar(depth, y_log, y_log_error, marker='o', color='k', linestyle='', markersize=4)

# uncomment to plot neutron intensity only
# plt.errorbar(depth, np.log(y_n), 1/np.sqrt(n_out), marker='o', color='r', linestyle='', markersize=4)
# plt.plot(depth, np.log(y_n))

plt.plot(depth[f_idx:], fit_fn(depth[f_idx:]))
plt.xlabel("Thickness (mm)")
plt.ylabel("Neutron Survival Fraction (Log)")
plt.title("Neutron Attenuation in concrete")
plt.show()


plt.plot(depth, y)
plt.errorbar(depth, y, np.sqrt(n_out)/n_in, marker='o', color='k', linestyle='')
plt.xlabel("Thickness (mm)")
plt.ylabel("Neutron Survival Fraction")
plt.title("Neutron Attenuation in concrete")
plt.show()
