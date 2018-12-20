import os
import numpy as np
import pandas as pd
import json

half_life = {
    'Be7':4590000,
    'C10':19.29,
    'C11':1220.00,
    'O14':70.60,
    'O15':122.24,
    'N13':597.9,
    'N16':7.13,
    'triton':2.69304e8,
    'F17':64.49,
    'C15':2.449,
    'F18':6586.2,
    'N17':4.173,
    'Be11':13.76,
    }
hour = 3600


def λ(key):
    return np.log(2)/half_life[key]


def ij(ZA, k):
    Z = ZA[0]
    A = ZA[1]
    N = A - Z
    return (Z-1,N-Z-k-1)


energies = np.linspace(0.2500, 0.0700, 19)
spread   = [0.1020,0.0979,0.0913,0.0790,0.0645,0.0540]
thickness = [3.]   # cm
actual_protons = 1e11
beam_time = 60  # 1 min beam time

isotope_ZA = {
    "triton":(1,3),
    "N13":(7,13),
    "F17":(9,17),
    "N16":(7,16),
    "C15":(6,15),
    "F18":(9,18),
    "N17":(7,17),
    "O15":(8,15),
    "Be11":(4,11),
    "C11":(6,11),
    "Be7":(4,7),
    "O14":(8,14),
    "C10":(6,10),
    }
isotopes = list(isotope_ZA.keys())


json_list = []
for n, e in enumerate(energies):
    for t in thickness:
        directory = "/{rThickness}-{bEnergy:.1f}/".format(rThickness=round(t), bEnergy=round(1000*e,1))
        with open(os.getcwd() + directory + "in001_fort.26", 'r') as f:
            lines = f.readlines()

            k = int(lines[12].split()[7])   # set k
            events = int(lines[5].split()[5][:-1])
            numbers = []
            data = lines[14:-1]

            for i in range(len(data)):
                data[i] = data[i].split()
            data = np.transpose(np.array(data))

            for iso in isotopes:
                #numbers = float(data[ij(isotope_ZA[iso], k)])*actual_protons
                numbers.append(float(data[ij(isotope_ZA[iso], k)])*events)
            #print(numbers)


            triton = {"halflife" : 2.69304e8, "lifeTime" : 1/λ('triton'),"number" : numbers[0]}
            N13 = {"halflife" : 597.9, "lifeTime" : 1/λ('N13'),"number" : numbers[1]}
            F17 = {"halflife" : 64.49, "lifeTime" : 1/λ('F17'),"number" : numbers[2]}
            N16 = {"halflife" : 7.13, "lifeTime" : 1/λ('N16'),"number" : numbers[3]}
            C15 = {"halflife" : 2.449, "lifeTime" : 1/λ('C15'),"number" : numbers[4]}
            F18 = {"halflife" : 6586.2, "lifeTime" : 1/λ('F18'),"number" : numbers[5]}
            N17 = {"halflife" : 4.173, "lifeTime" : 1/λ('N17'),"number" : numbers[6]}
            O15 = {"halflife" : 122.24, "lifeTime" : 1/λ('O15'),"number" : numbers[7]}
            Be11 = {"halflife" : 13.76, "lifeTime" : 1/λ('Be11'),"number" : numbers[8]}
            C11 = {"halflife" : 1220.00, "lifeTime" : 1/λ('C11'),"number" : numbers[9]}
            Be7 = {"halflife" : 4590000, "lifeTime" : 1/λ('Be7'),"number" : numbers[10]}
            O14 = {"halflife" : 70.60, "lifeTime" : 1/λ('O14'),"number" : numbers[11]}
            C10 = {"halflife" : 19.29, "lifeTime" : 1/λ('C10'),"number" : numbers[12]}

            isotopes_json = {
                "triton":triton,
                "N13":N13,
                "F17":F17,
                "N16":N16,
                "C15":C15,
                "F18":F18,
                "N17":N17,
                "O15":O15,
                "Be11":Be11,
                "C11":C11,
                "Be7":Be7,
                "O14":O14,
                "C10":C10
                }

            dict = {
                'run':n,
                'nEvents':events,
                'energy':e,
                'physicsList':"HADROTHErapy",
                'rangeshifterThickness':t,
                'isotopes':isotopes_json
                }

            json_list.append(dict)

print(json.dumps(json_list, indent=4))
