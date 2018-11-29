import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import simps

hour = 3600

energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # MeV
spread   = [0.1020,0.0979,0.0913,0.0790,0.0645,0.0540]
thickness = [1.,2.,3.,5.]   # cm

input_protons  = 1e7
actual_protons = 1e11
beam_time = 60  # 1 min beam time

rows = []
mean=[]

def rectangular(data, dx=1.0):
    return np.sum(np.asarray(data)*dx)

def gaussian(mean, std=1):
    return lambda x: 1./(np.sqrt(2.*np.pi)*std)*np.exp(-np.power((x - mean)/std, 2.)/2)


# Loop over every energy & thickness
for i, e in enumerate(energies):
    binwidth = 2*e*1000/140  # Gev
    for t in thickness:
        directory = "/{rThickness}-{bEnergy:03}/".format(rThickness=round(t), bEnergy=round(1000*e))
        # Read uprange data
        with open(os.getcwd() + directory + "in001_fort.27", 'r') as f:

            lines = f.readlines()
            mergedata = []
            data = []
            data = lines[17:31]
            for i in range(len(data)):
                data[i] = data[i].split()
            for i in range(len(data)):
                mergedata = mergedata + data[i]

            mergedata = np.array(mergedata, dtype=float)
            mergedata = mergedata / rectangular(mergedata, dx=binwidth)


        # Open downrange data
        with open(os.getcwd() + directory + "in001_fort.28", 'r') as g:
            lines2 = g.readlines()
            mergedata2 = []
            data2 = []
            data2 = lines2[17:31]
            for i in range(len(data2)):
                data2[i] = data2[i].split()
            for i in range(len(data2)):
                mergedata2 = mergedata2 + data2[i]

            mergedata2 = np.array(mergedata2, dtype=float)
            mergedata2 = mergedata2 / rectangular(mergedata2, dx=binwidth)

        length = np.linspace(0,(139*binwidth),num=140) + binwidth/2

        # ==== Plot the results ====
        plt.bar(x=length,height=mergedata, width=binwidth, color=(0.4,0.4,1))       # Uprange
        plt.bar(x=length,height=mergedata2, width=binwidth, color=(1,0.1,0.1,0.6))  # Downrange

        # Annotations
        plt.xlabel("Energy (GeV)")
        plt.ylabel("Ratio of number of protons leaving to number of protons entering")
        plt.title("E= {:.3f} MeV, x= {:.3f} cm".format(e, t))

        print("E= {:.3f} MeV, x= {:.3f} cm".format(e, t))

        print("Area = {}".format(rectangular(mergedata, dx=binwidth)))

        # Calculate
        totalp = []

        meanE = np.sum([mergedata[i]*length[i] for i in range(len(mergedata))])/np.sum(mergedata)

        print(meanE)

        varE = np.sum([mergedata[i]*np.square(length[i]-meanE) for i in range(len(mergedata))])/(np.sum(mergedata))
        shepcor = varE - np.square(binwidth)/12
        print(np.sqrt(shepcor))

        # Plot the reconstructed gaussian for the uprange proton energy distribution
        y = gaussian(meanE, std=np.sqrt(shepcor))(length)
        plt.plot(length, y)
        plt.show()
        """
        for i in range(len(mergedata)):
            totalp.append((mergedata[i])*(length[i]))
        print(sum(totalp)/(sum(mergedata)) - binwidth/2)

         for i in range(len(mergedata)):
            totalp.append(mergedata[i]*np.square(length[i]-meanE))
        print(sum(totalp)/(sum(mergedata)-1))

        """
