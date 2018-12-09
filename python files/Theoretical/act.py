import numpy as np
import pandas as pd
import matplotlib as plt


dir = 'data/'
mb = 1e-3 * 1e-24  # millibarns in cm2

half_life = {'Be7':4590000, 'C10':19.29, 'C11':1220.00, 'O14':70.60, 'O15':122.24}
hour = 3600
beam_time = 60


def λ(key):
    return np.log(2)/half_life[key]


C12 = {
     70:{'Be7':21*mb,'C10':0*5*mb,'C11':75*mb,'O14':0*mb,'O15':0},
    100:{'Be7':17*mb,'C10':0*5*mb,'C11':62*mb,'O14':0*mb,'O15':0},
    150:{'Be7':14*mb,'C10':0*5*mb,'C11':45*mb,'O14':0*mb,'O15':0},
    200:{'Be7':10*mb,'C10':0*4*mb,'C11':41*mb,'O14':0*mb,'O15':0},
    230:{'Be7':10*mb,'C10':0*4*mb,'C11':38*mb,'O14':0*mb,'O15':0},
    250:{'Be7':10*mb,'C10':0*4*mb,'C11':37*mb,'O14':0*mb,'O15':0}
}

O16 = {
     70:{'Be7':9*mb, 'C10':4*mb,'C11':18*mb,'O14':1*mb,'O15':71*mb},
    100:{'Be7':6*mb, 'C10':6*mb,'C11':15*mb,'O14':1*mb,'O15':61*mb},
    150:{'Be7':8*mb, 'C10':2*mb,'C11':11*mb,'O14':1*mb,'O15':42*mb},
    200:{'Be7':8*mb, 'C10':2*mb,'C11':11*mb,'O14':1*mb,'O15':41*mb},
    230:{'Be7':8*mb, 'C10':2*mb,'C11':10*mb,'O14':1*mb,'O15':40*mb},
    250:{'Be7':8*mb, 'C10':2*mb,'C11':10*mb,'O14':1*mb,'O15':39*mb}
}

elemFraction = {'C12':0.41, 'O16':0.13}  # elemental fractions of Carbon-12 and Oxygen-16
n = 9.7e22                               # number density of target

isotopes = half_life.keys()

thickness = [1,2,3,5]
energies = [70,100,150,200,230,250]
N = 1e11

rows = []

for i, e in enumerate(energies):
    for t in thickness:
        dict = {'energy':e, 'thickness':t}
        for iso in isotopes:
            dict[iso] = np.sum(
               [ elemFraction['C12'] * N * C12[e][iso] * n * t,
                 elemFraction['O16'] * N * O16[e][iso] * n * t
               ]
            )

        rows.append(dict)

df = pd.DataFrame(rows)

# normalise data to beam
df.to_csv(dir + "normalized.csv")

# find saturation values
saturation = df.copy()
for ist in isotopes:
    print(ist, end=' ')
    print(λ(ist))
    saturation[ist] = saturation[ist] * (1 - np.exp(-λ(ist)*beam_time)) / beam_time

print(saturation)
saturation.to_csv(dir + "saturation.csv")

# find one hour values
one_hour_value = saturation.copy()
for ist in isotopes:
    one_hour_value[ist] = one_hour_value[ist] * np.exp(-λ(ist)*1*hour)
