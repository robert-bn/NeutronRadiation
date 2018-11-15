import numpy as np
import pandas as pd

hour = 3600
half_life = {'Be7':4590000, 'C10':19.29, 'C11':1220.00, 'O14':70.60, 'O15':122.24, 'F17':64.49}

input_protons  = 1e7
actual_protons = 1e11
beam_time = 60  # 1 min beam time

def λ(key):
    return np.log(2)/half_life[key]


data = pd.read_json("out.json")

# "important" isotopes, i.e. those with half life 1s < t < 10 years &
# appriciable amount created.

imp_ist = list(half_life.keys())

data = data[['thickness (cm)', 'energy'] + imp_ist].sort_index()

# normalise data to beam
data[imp_ist] = data[imp_ist] * actual_protons / input_protons


# find saturation values
saturation = data.copy()
for ist in half_life.keys():
    saturation[ist] = saturation[ist] * (1 - np.exp(-λ(ist)*beam_time))

print(saturation)
saturation.to_csv("saturation.csv")

# find one hour values
one_hour_value = saturation.copy()
for ist in half_life.keys():
    one_hour_value[ist] = one_hour_value[ist] * np.exp(-λ(ist)*1*hour)

print(one_hour_value)
one_hour_value.to_csv("one hour value.csv")
