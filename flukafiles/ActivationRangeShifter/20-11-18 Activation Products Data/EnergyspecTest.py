import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

hour = 3600

energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # MeV
spread   = [0.1020,0.0979,0.0913,0.0790,0.0645,0.0540]
thickness = [1.,2.,3.,5.]   # cm

input_protons  = 1e7
actual_protons = 1e11
beam_time = 60  # 1 min beam time

rows = []

for i, e in enumerate(energies):
    for t in thickness:
        with open("template.txt", 'r') as templatef:
            directory = "/{rThickness}-{bEnergy:03}/".format(rThickness=round(t), bEnergy=round(1000*e))
            with open(os.getcwd() + directory + "in001_fort.28", 'r') as f:
                lines = f.readlines()

                mergedata = []
                data = []
                data = lines[17:-1]
                for i in range(len(data)):
                    data[i] = data[i].split()
                for i in range(len(data)):
                    mergedata = mergedata + data[i]
                for i in range(len(mergedata)):
                    mergedata[i]=float(mergedata[i])

                length = np.linspace(1,60,num=60)
                plt.bar(x=length,height=mergedata)
                plt.xlabel("Energy (GeV)")
                plt.ylabel("Differential Fluence per Energy (cm^-2 sr^-1 GeV^-1)")
                plt.title("E=70MeV, x=1cm")
                plt.show()


df = pd.DataFrame(mergedata)

range = np.linspace(1,60,num=60)
plt.bar(x=range,height=mergedata)
plt.xlabel("Energy (GeV)")
plt.ylabel("Differential Fluence per Energy (cm^-2 sr^-1 GeV^-1)")
plt.title("E=70MeV, x=1cm")
plt.show()

df.to_csv("Test.csv")