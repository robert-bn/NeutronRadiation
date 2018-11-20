import os
import numpy as np
import pandas as pd

def ij(ZA, k):
    Z = ZA[0]
    A = ZA[1]
    N = A - Z
    return (Z-1,N-Z-k-1)


energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # MeV
spread   = [0.1020,0.0979,0.0913,0.0790,0.0645,0.0540]
thickness = [1.,2.,3.,5.]   # cm

isotope_ZA = {"Be7":(4,7), "C10":(6,10), "C11":(6,11), "O14":(8,14), "O15":(8, 15), "F17":(9, 17)}
isotopes = ["Be7", "C10", "C11", "O14", "O15", "F17"]

rows = []

for i, e in enumerate(energies):
    for t in thickness:
        with open("template.txt", 'r') as templatef:
            directory = "/{rThickness}-{bEnergy:03}/".format(rThickness=round(t), bEnergy=round(1000*e))
            with open(os.getcwd() + directory + "in001_fort.26", 'r') as f:
                lines = f.readlines()
                k = int(lines[12].split()[7])   # set k

                data = lines[14:-1]
                for i in range(len(data)):
                    data[i] = data[i].split()

                data = np.transpose(np.array(data))
                dict = {'energy':e, 'thickness':t}

                for iso in isotopes:
                    dict[iso] = data[ij(isotope_ZA[iso], k)]

                rows.append(dict)

df = pd.DataFrame(rows)
df.to_csv("activation (FLUKA).csv")
