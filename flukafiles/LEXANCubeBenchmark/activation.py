import os
import numpy as np
import pandas as pd

half_life = {'Be7':4590000, 'C10':19.29, 'C11':1220.00, 'O14':70.60, 'O15':122.24, 'F17':64.49}
threeminutes = 120
oneminute = 60
fiveminutes = 300


def λ(key):
    return np.log(2)/half_life[key]


def ij(ZA, k):
    Z = ZA[0]
    A = ZA[1]
    N = A - Z
    return (Z-1,N-Z-k-1)


energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # MeV
spread   = [0.1020,0.0979,0.0913,0.0790,0.0645,0.0540]
thickness = [1.]   # cm

input_protons  = 1e7
actual_protons = 1e11
beam_time = 60  # 1 min beam time

isotope_ZA = {"Be7":(4,7), "C10":(6,10), "C11":(6,11), "O14":(8,14), "O15":(8, 15), "F17":(9, 17)}
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

# find two minutes values
two_minutes_value = saturation.copy()
for ist in isotopes:
    two_minutes_value[ist] = two_minutes_value[ist] * np.exp(-λ(ist)*1*threeminutes)
    two_minutes_value[ist + " error"] = two_minutes_value[ist + " error"] * np.exp(-λ(ist)*1*threeminutes)


print(two_minutes_value)
two_minutes_value.to_csv("two minutes value (FLUKA).csv")

# find one minute values
one_minute_value = saturation.copy()
for ist in isotopes:
    one_minute_value[ist] = one_minute_value[ist] * np.exp(-λ(ist)*1*oneminute)
    one_minute_value[ist + " error"] = one_minute_value[ist + " error"] * np.exp(-λ(ist)*1*oneminute)


print(one_minute_value)
one_minute_value.to_csv("one minute value (FLUKA).csv")

# find five minutes values
five_minutes_value = saturation.copy()
for ist in isotopes:
    five_minutes_value[ist] = five_minutes_value[ist] * np.exp(-λ(ist)*1*fiveminutes)
    five_minutes_value[ist + " error"] = five_minutes_value[ist + " error"] * np.exp(-λ(ist)*1*fiveminutes)


print(five_minutes_value)
five_minutes_value.to_csv("five minutes value (FLUKA).csv")
