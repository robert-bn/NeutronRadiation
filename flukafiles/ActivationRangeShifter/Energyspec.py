import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # GeV
thickness = [1.,2.,3.,5.]   # cm

# Arrays for the output dataframe
pandEnergy    = []
pandThickness = []
pandMeanup    = []
pandMean      = []
pandStdup     = []
pandStd       = []
pandRatio     = []


def rectangular(data, dx=1.0):
    return np.sum(np.asarray(data)*dx)


def gaussian(mean, std=1):
    return lambda x: 1./(np.sqrt(2.*np.pi)*std)*np.exp(-np.power((x - mean)/std, 2.)/2)


def read_data(filename, directory=''):
    # function to read data from _fort.XX file
    with open(os.getcwd() + directory + filename, 'r') as f:
        lines = f.readlines()

    freq = []
    data = []
    data = lines[17:82]

    # Histogram raneg and bins in GeV
    binwidth = float(lines[13].split()[11])
    xmin = float(lines[13].split()[4])
    xmax = float(lines[13].split()[6])

    bin_num = float(lines[13].split()[8])  # number of bins

    # Read data into arrays
    for i in range(len(data)):
        data[i] = data[i].split()
    for i in range(len(data)):
        freq = freq + data[i]

    freq = np.array(freq, dtype=float)

    # Normalise data
    freq = freq / rectangular(freq, dx=binwidth)

    energy = np.linspace(xmin,xmax,num=bin_num) + binwidth/2

    return freq, energy, binwidth



# Loop over every energy & thickness
for i, e in enumerate(energies):
    for t in thickness:
        dir = "/{rThickness}-{bEnergy:03}/".format(rThickness=round(t), bEnergy=round(1000*e))
        # Read uprange data
        freqUprange, energy, binwidth = read_data("in001_fort.27", directory=dir)

        # Open downrange data
        freqDownrange = read_data("in001_fort.28", directory=dir)[0]



        # ==== Plot the results ====
        plt.bar(x=energy,height=freqUprange, width=binwidth, color=(0.4,0.4,1))       # Uprange
        plt.bar(x=energy,height=freqDownrange, width=binwidth, color=(1,0.1,0.1,0.6))  # Downrange

        # Annotations
        plt.xlabel("Kinetic Energy (MeV)")
        plt.ylabel("Probability Density of Proton Kinetic Energy")
        plt.title("E= {:.3f} GeV, x= {:.3f} cm".format(e, t))

        # Calculate mean & varience of upstream data
        meanupE = np.sum([freqUprange[i]*energy[i] for i in range(len(freqUprange))])/np.sum(freqUprange)

        varupE = np.sum([freqUprange[i]*np.square(energy[i]-meanupE) for i in range(len(freqUprange))])/(np.sum(freqUprange))
        shepcorup = varupE - np.square(binwidth)/12

        # Find the index that contains the mean
        meanarg = np.argmax(freqDownrange)

        # Calculate mean & varience of downstream data (about the mean)
        meanE = np.sum([freqDownrange[i]*energy[i] for i in range((meanarg - 30), (meanarg + 30))])/np.sum(freqDownrange[meanarg - 30 + i] for i in range(0,60))
        varE = np.sum([freqDownrange[i]*np.square(energy[i]-meanE) for i in range((meanarg - 30), len(freqDownrange))])/(np.sum(freqDownrange[meanarg - 30 + i] for i in range(0,60)))
        #meanE = np.sum([freqDownrange[i]*energy[i] for i in range(0, len(freqDownrange))])/np.sum(freqDownrange[i] for i in range(0,len(freqDownrange)))
        #varE = np.sum([freqDownrange[i]*np.square(energy[i]-meanE) for i in range(0, len(freqDownrange))])/np.sum(freqDownrange[i] for i in range(0,len(freqDownrange)))
        shepcor = varE - np.square(binwidth)/12

        # Calculate ratio of no. of downsteam to upstream protons
        ratio = float(lines2[92])*100*2*np.pi*300

        # Print some useful information
        print("E= {:.3f} GeV, x= {:.3f} cm".format(e, t)) # Enegy and thickness
        print("Area = {}".format(rectangular(freqDownrange, dx=binwidth))) # Normalised area
        print("Mean energy = {}".format(meanE)) # Mean Energy
        print(np.sqrt(varE)) # Standard Deviation
        print(np.sqrt(shepcor)) # Corrected Standard Deviation
        print(ratio) # Number of downstream protons relative to upstream protons

        # Plot the reconstructed gaussian for the uprange proton energy distribution
        y = gaussian(meanE, std=np.sqrt(shepcor))(energy)
        plt.plot(energy, y)
        plt.show()

        pandEnergy.append(e)
        pandThickness.append(t)
        pandMeanup.append(meanupE)
        pandStdup.append(np.sqrt(shepcorup))
        pandMean.append(meanE)
        pandStd.append(np.sqrt(shepcor))
        pandRatio.append(ratio)



energyspecdata ={
    "Kinetic Energy (GeV)" : pandEnergy,
    "Thickness (cm)" : pandThickness,
    "Upstream Energy Mean (GeV)" : pandMeanup,
    "Downstream Energy Mean (GeV)" : pandMean,
    "Upstream Energy Std" : pandStdup,
    "Downstream Energt Std" : pandStd,
    "Ratio" : pandRatio
}
df = pd.DataFrame(energyspecdata)
print(df)
#df.to_csv("DownrangeEnergySpectra(FLUKA).csv")
