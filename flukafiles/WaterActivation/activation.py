import os
import numpy as np
import pandas as pd

half_life = {'Be7':4590000, 'C10':19.29, 'C11':1220.00, 'O14':70.60, 'O15':122.24, 'N13':597.9, 'N16':7.13}
hour = 3600


def λ(key):
    return np.log(2)/half_life[key]


def ij(ZA, k):
    Z = ZA[0]
    A = ZA[1]
    N = A - Z
    return (Z-1,N-Z-k-1)


energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # MeV
spread   = [0.1020,0.0979,0.0913,0.0790,0.0645,0.0540]
thickness = [1.,2.,3.,5.]   # cm

input_protons  = 1e6
actual_protons = 1e11
beam_time = 60  # 1 min beam time

isotope_ZA = {"Be7":(4,7), "C10":(6,10), "C11":(6,11), "O14":(8,14), "O15":(8, 15), "N13":(7, 13), "N16":(7, 16)}
isotopes = list(isotope_ZA.keys())


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
                    dict[iso] = float(data[ij(isotope_ZA[iso], k)])
                    dict[iso + " error"] = np.sqrt(float(data[ij(isotope_ZA[iso], k)]) / input_protons) * actual_protons

                rows.append(dict)


df = pd.DataFrame(rows)
df = df.sort_values(by=["thickness","energy"], ascending=[True,False])


# normalise data to beam
df[isotopes] = actual_protons * df[isotopes]
df.to_csv("normalized N (FLUKA).csv")

# find saturation values
saturation = df.copy()
for ist in isotopes:
    print(ist, end=' ')
    print(λ(ist))
    saturation[ist] = saturation[ist] * (1 - np.exp(-λ(ist)*beam_time)) / beam_time
    saturation[ist + " error"] = saturation[ist + " error"] * (1 - np.exp(-λ(ist)*beam_time)) / beam_time

print(saturation)
saturation.to_csv("saturation (FLUKA).csv")

# find one hour values
one_hour_value = saturation.copy()
for ist in isotopes:
    one_hour_value[ist] = one_hour_value[ist] * np.exp(-λ(ist)*1*hour)
    one_hour_value[ist + " error"] = one_hour_value[ist + " error"] * np.exp(-λ(ist)*1*hour)


print(one_hour_value)
one_hour_value.to_csv("one hour value (FLUKA).csv")
