import os
import numpy as np
import pandas as pd
import json

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


for n, e in enumerate(energies):
    for t in thickness:
        with open("template.txt", 'r') as templatef:
            directory = "/{rThickness}-{bEnergy:03}/".format(rThickness=round(t), bEnergy=round(1000*e))
            with open(os.getcwd() + directory + "in001_fort.26", 'r') as f:
                lines = f.readlines()
                k = int(lines[12].split()[7])   # set k
                events = lines[5].split()[5][:-1]
                numbers = []

                data = lines[14:-1]
                for i in range(len(data)):
                    data[i] = data[i].split()

                data = np.transpose(np.array(data))
                
                for iso in isotopes:
                    #numbers = float(data[ij(isotope_ZA[iso], k)])*actual_protons
                    numbers.append(float(data[ij(isotope_ZA[iso], k)])*actual_protons)
                #print(numbers)
                
                Be7 = {"halflife" : 4590000, "lifeTime" : 1/λ('Be7'),"number" : numbers[0]}
                C10 = {"halflife" : 19.29, "lifeTime" : 1/λ('C10'),"number" : numbers[1]}
                C11 = {"halflife" : 1220.00, "lifeTime" : 1/λ('C11'),"number" : numbers[2]}
                O14 = {"halflife" : 70.60, "lifeTime" : 1/λ('O14'),"number" : numbers[3]}
                O15 = {"halflife" : 122.24, "lifeTime" : 1/λ('O15'),"number" : numbers[4]}
                N13 = {"halflife" : 597.9, "lifeTime" : 1/λ('N13'),"number" : numbers[5]}
                N16 = {"halflife" : 7.13, "lifeTime" : 1/λ('N16'),"number" : numbers[6]}

                isotopes_json = {"Be7":Be7, "C10":C10, "C11":C11, "O14":O14, "O15":O15, "N13":N13, "N16":N16}

                dict = {
                    'run':n, 
                    'nevents':events,
                    'energy':e,
                    'thickness':t,
                    'physicsList':"HADROTHErapy",
                    'isotopes':isotopes_json
                    }


                print(json.dumps(dict, indent=4))




