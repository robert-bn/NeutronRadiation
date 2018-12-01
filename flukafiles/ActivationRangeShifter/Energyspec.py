import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy.ma as ma

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
    for t in thickness:
        directory = "/{rThickness}-{bEnergy:03}/".format(rThickness=round(t), bEnergy=round(1000*e))
        # Read uprange data
        with open(os.getcwd() + directory + "in001_fort.27", 'r') as f:

            lines = f.readlines()
            mergedata = []
            data = []
            data = lines[17:82]
            
            binwidth = float(lines[13].split()[11])  # Gev
            xmin = float(lines[13].split()[4])
            xmax = float(lines[13].split()[6])
            binno = float(lines[13].split()[8])

            
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
            data2 = lines2[17:82]
            
            for i in range(len(data2)):
                data2[i] = data2[i].split()
            for i in range(len(data2)):
                mergedata2 = mergedata2 + data2[i]

            mergedata2 = np.array(mergedata2, dtype=float)
            mergedata2 = mergedata2 / rectangular(mergedata2, dx=binwidth)

        length = np.linspace(xmin,xmax,num=binno) + binwidth/2

        # ==== Plot the results ====
        plt.bar(x=length,height=mergedata, width=binwidth, color=(0.4,0.4,1))       # Uprange
        plt.bar(x=length,height=mergedata2, width=binwidth, color=(1,0.1,0.1,0.6))  # Downrange

        # Annotations
        plt.xlabel("Kinetic Energy (MeV)")
        plt.ylabel("Probability Density of Proton Kinetic Energy")
        plt.title("E= {:.3f} GeV, x= {:.3f} cm".format(e, t))

        '''
        # Calculate mean & varience of data
        meanE = np.sum([mergedata[i]*length[i] for i in range(len(mergedata))])/np.sum(mergedata)

        varE = np.sum([mergedata[i]*np.square(length[i]-meanE) for i in range(len(mergedata))])/(np.sum(mergedata))
        shepcor = varE - np.square(binwidth)/12#
        '''

        # Calculate mean & varience of data
        meanarg = np.argmax(mergedata2)


        meanE = np.sum([mergedata2[i]*length[i] for i in range((meanarg - 30), (meanarg + 30))])/np.sum(mergedata2[meanarg - 30 + i] for i in range(0,60))
        #print(mergedata2[350])
        varE = np.sum([mergedata2[i]*np.square(length[i]-meanE) for i in range((meanarg - 30), len(mergedata2))])/(np.sum(mergedata2[meanarg - 30 + i] for i in range(0,60)))
        shepcor = varE - np.square(binwidth)/12
        

        # Print some useful information
        print("E= {:.3f} GeV, x= {:.3f} cm".format(e, t))
        print("Area = {}".format(rectangular(mergedata2, dx=binwidth)))
        print("Mean energy = {}".format(meanE))
        print(np.sqrt(varE))
        print(np.sqrt(shepcor))

        # Plot the reconstructed gaussian for the uprange proton energy distribution
        y = gaussian(meanE, std=np.sqrt(shepcor))(length)
        plt.plot(length, y)
        plt.show()
        """
        totalp = []
        for i in range(len(mergedata)):
            totalp.append((mergedata[i])*(length[i]))
        print(sum(totalp)/(sum(mergedata)) - binwidth/2)

         for i in range(len(mergedata)):
            totalp.append(mergedata[i]*np.square(length[i]-meanE))
        print(sum(totalp)/(sum(mergedata)-1))

        """
