# reads in a g4beamline output TEXT file, and plots the number of protons at each z vs distance
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

NEUTRON_PDGid = 2112
NeutronsOnly=True

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
        if NeutronsOnly==True:
            n_out.append(np.count_nonzero(df['PDGid']==NEUTRON_PDGid))

n_out = np.array(n_out)
y = n_out/n_in
y_log = np.log(n_out/n_in)
y_log_error = 1/np.sqrt(n_out)
f_idx = 11 # first index to calculate regression from
l_idx = 20 # last index  to calculate regression from

fit, cov = np.polyfit(depth[f_idx:l_idx],y_log[f_idx:l_idx],1,w=1/y_log_error[f_idx:l_idx]**2, cov=True)  # don't include first 6 points in regression
fit_fn = np.poly1d(fit)

x_ = np.array([1,0])
y_ = np.array([0,1])

errorx = np.dot(x_, np.dot(cov, x_))
errory = np.dot(y_, np.dot(cov, y_))

chi2 = np.sum( (y_log[f_idx:l_idx] - fit_fn(depth[f_idx:l_idx])) ** 2 / y_log_error[f_idx:l_idx]**2)
red_chi2 = chi2/(len(depth) - f_idx - 2)
print("fitting parameters: {}".format(fit))
print("error: {}".format([errorx, errory]))
print("chi^2: {}".format(chi2))
print("reduced chi^2: {}".format(red_chi2))
print("half value layer: ( {}±{} )mm".format(-np.log(2)/fit[0], -np.log(2)/fit[0]**2 * errorx))
print("tenth value layer: ( {}±{} )mm".format(-np.log(10)/fit[0], -np.log(10)/fit[0]**2 * errorx))
# plot data
# plt.plot(depth, np.log(y))

plt.errorbar(depth, y_log, y_log_error, marker='o', color='k', linestyle='', markersize=4)

# uncomment to plot neutron intensity only
# plt.errorbar(depth, np.log(y_n), 1/np.sqrt(n_out), marker='o', color='r', linestyle='', markersize=4)
# plt.plot(depth, np.log(y_n))

plt.plot(depth[f_idx:l_idx], fit_fn(depth[f_idx:l_idx]))
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
