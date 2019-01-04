import os
from numpy import sqrt, linspace

# energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # GeV
# spread   = [0.1020,0.0979,0.0913,0.0790,0.0645,0.0540]
# bins = [0.30,0.28,0.25,0.20,0.15,0.12]
# bins2 = [0.17,0.15,0.12,0.06,0.00,0.00]
# energies = linspace(0.250, 0.07, 19)
energies = [0.06,0.05,0.04,0.03,0.02,0.01]
# runs = linspace(3000000.0, 21000000, 19)
runs = linspace(22000000, 27000000, 6)
#bins = linspace(0.30, 0.12, 19)
bins = [0.12,0.12,0.12,0.12,0.12,0.12]
#bins2 = linspace(0.17, -0.01, 19)
bins2 = [0.00,0.00,0.00,0.00,0.00,0.00]
thickness = [1.]   # cm

m_p = .938  # GeV

def spread(T, δ=0.004):
    # returns energy spread in GeV
    E = T + m_p
    return 2.335 *  δ * T * E / sqrt(E**2 - m_p**2)


def create_files():
    for i, e in enumerate(energies):
        for t in thickness:
            with open("template.txt", 'r') as templatef:
                directory = "/{rThickness}-{bEnergy:03}/".format(rThickness=round(t), bEnergy=round(1000*e))
                os.makedirs(os.getcwd() + directory)
                with open(os.getcwd() + directory + "in.inp", 'w+') as f:
                    for line in templatef:
                        line = line.replace("$rThickness$",str(t))
                        line = line.replace("$bEnergy$","{:.6f}".format(e))
                        line = line.replace("$bEnergySpread$","{:.6f}".format(spread(e)))
                        line = line.replace("$bRuns$","{:.8}".format(str(runs[i])))
                        line = line.replace("$cBins$","{:.2f}").format(bins2[i])
                        line = line.replace("$bBins$","{:.2f}".format(bins[i]))
                        line = line.replace("$aEnergy$","{:.2f}".format(e))
                        line = line.replace("$aThickness$",str(t))
                        print(line, file=f, end='')

create_files()
