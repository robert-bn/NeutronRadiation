import numpy as np
import pandas as pd
from decimal import Decimal


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

# errors
for ist in half_life.keys():
    data[ist + " error"] = np.sqrt(data[ist]) * actual_protons / input_protons

# normalise data to beam
data[imp_ist] = data[imp_ist] * actual_protons / input_protons
data.to_csv("normalized.csv")

# find saturation values
saturation = data.copy()
for ist in half_life.keys():
    print(ist, end=' ')
    print(λ(ist))
    saturation[ist] = saturation[ist] * (1 - np.exp(-λ(ist)*beam_time)) / beam_time
    saturation[ist + " error"] = saturation[ist + " error"] * (1 - np.exp(-λ(ist)*beam_time)) / beam_time

print(saturation)
saturation.to_csv("saturation.csv")

# find one hour values
one_hour_value = saturation.copy()
for ist in half_life.keys():
    one_hour_value[ist] = one_hour_value[ist] * np.exp(-λ(ist)*1*hour)
    one_hour_value[ist + " error"] = one_hour_value[ist + " error"] * np.exp(-λ(ist)*1*hour)

print(one_hour_value)
one_hour_value.to_csv("one hour value.csv")

ist_name = {'Be7':'Be', 'C10':'C', 'C11':'C', 'O14':'O', 'O15':'O', 'F17':'F'}
ist_num = {'Be7':7, 'C10':10, 'C11':11, 'O14':14, 'O15':15, 'F17':15}

superscript_d = {0:'⁰', 1:'¹', 2:'²', 3:'³', 4:'⁴', 5:'⁵', 6:'⁶', 7:'⁷', 8:'⁸', 9:'⁹'}

prefix = {0:'', 3:'k', 6:'M', 9:'B'}

def superscript(x):
    super = ""
    for char in str(x):
        super += str(superscript_d[int(char)])
    return super


def formatnum(x, unit='', SIprefix=False, err=None):
    if x < 1e-9:
        return 0
    exponent = int(np.floor(np.log10(x)))
    if SIprefix:
        prefix_exponent = int(3*np.floor(exponent / 3))
        y = x / np.power(10, prefix_exponent)
        if err is not None:
            erry = err / np.power(10, prefix_exponent)
            return "({:.2f}±{}) ".format(y, round(erry,2)) + prefix[prefix_exponent] + unit
        else:
            return "{:.2f} ".format(y) + prefix[prefix_exponent] + unit
    else:
        y = x / np.power(10, exponent)
        if err is not None:
            erry = err / np.power(10, exponent)
            print(round(erry,2))
            return "({:.2f}±{})×10{} ".format(y, round(erry,2), superscript(exponent)) + unit
        else:
            return "{:.2f}×10{} ".format(y, superscript(exponent)) + unit

def errformat(x, err, unit):
    exponent = int(np.floor(np.log10(x)))
    y = x / np.power(10, exponent)
    return "({:.2f}±{:.2f})×10{} ".format(y, superscript(exponent)) + unit

def print_tables():
    with open("pretty_tables1.csv", 'w') as f:
        f.write(" , Half Life (s), Number of particles produced, ,Activity\n")
        f.write(" , , 230 MeV, 200 MeV, 230 MeV, 200 MeV\n")
        n230 = data[(data['thickness (cm)'] == 2) & (data['energy'] == 230)]
        n200 = data[(data['thickness (cm)'] == 2) & (data['energy'] == 200)]
        a230 = saturation[(data['thickness (cm)'] == 2) & (data['energy'] == 230)]
        a200 = saturation[(data['thickness (cm)'] == 2) & (data['energy'] == 200)]

        for ist in half_life.keys():
            print(ist)
            f.write(superscript(ist_num[ist]))
            f.write(ist_name[ist])
            f.write(",{halflife},{num230},{num200},{act230},{act200}".format(
                halflife=formatnum(half_life[ist], ''),
                num230 = formatnum(n230[ist].iloc[0], err=n230[ist + " error"].iloc[0]),
                num200 = formatnum(n200[ist].iloc[0], err=n200[ist + " error"].iloc[0]),
                act230 = formatnum(a230[ist].iloc[0], unit='Bq', SIprefix=True, err=a230[ist + " error"].iloc[0]),
                act200 = formatnum(a200[ist].iloc[0], unit='Bq', SIprefix=True, err=a230[ist + " error"].iloc[0])
            ))
            f.write("\n")

    with open("pretty_tables2.csv", 'w') as f:
        f.write(" ,Activity, \n")
        f.write(" , 230 MeV, 200 MeV\n")
        s230 = one_hour_value[(data['thickness (cm)'] == 2) & (data['energy'] == 230)]
        s200 = one_hour_value[(data['thickness (cm)'] == 2) & (data['energy'] == 200)]

        for ist in ['Be7', 'C11']:
            print(ist)
            f.write(superscript(ist_num[ist]))
            f.write(ist_name[ist])
            f.write(",{act230},{act200}".format(
                halflife=formatnum(half_life[ist], ''),
                act230 = formatnum(s230[ist].iloc[0], unit='Bq', SIprefix=True, err=s230[ist + " error"].iloc[0]),
                act200 = formatnum(s200[ist].iloc[0], unit='Bq', SIprefix=True, err=s230[ist + " error"].iloc[0])
            ))
            f.write("\n")
