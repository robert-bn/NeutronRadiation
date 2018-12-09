import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # GeV
thickness = [1.,2.,3.,5.]   # cm

# boolean settings
plotting = True
writecsv = False

# Arrays for the output dataframe
pandEnergy        = []
pandThickness     = []
pandMeanUprange   = []
pandMeanDownrange = []
pandStdUprange    = []
pandStdDownrange  = []
pandRatio         = []


def rectangular(data, dx=1.0):
    return np.sum(np.asarray(data)*dx)


def gaussian(mean, std=1):
    return lambda x: 1./(np.sqrt(2.*np.pi)*std)*np.exp(-np.power((x - mean)/std, 2.)/2)


def read_data(filename, directory='', normalization=None):
    # function to read data from _fort.XX file
    with open(os.getcwd() + directory + filename, 'r') as f:
        lines = f.readlines()

    freq = []
    data = []
    data = lines[17:82]

    # Histogram raneg and bins in GeV
    binWidth = float(lines[13].split()[11])
    xmin = float(lines[13].split()[4])
    xmax = float(lines[13].split()[6])

    binNum = float(lines[13].split()[8])  # number of bins

    # Read data into arrays
    for i in range(len(data)):
        data[i] = data[i].split()
    for i in range(len(data)):
        freq = freq + data[i]

    freq = np.array(freq, dtype=float)

    area = rectangular(freq, dx=binWidth)

    # Normalise data
    if normalization == 'auto':
        # normalise area to 1
        norm = 1 / area
    elif normalization is None:
        norm = 1.0
    else:
        try:
            # normalise area according to supplied argument
            norm = normalization
            # area = area * norm
        except TypeError:
            print("Warning: normalization keyword arg must be a numeric type.")
            norm = float('NaN')

    freq = freq * norm
    energy = np.linspace(xmin,xmax,num=binNum) + binWidth/2

    return freq, energy, binWidth, area


def _mean(data, freq):
    # return mean of binned data
    return np.sum(freq * data) / np.sum(freq)


def _var(data, freq, mean=None):
    # return varience of mean data
    if mean is None:
        mean = _mean(data, freq)

    return np.sum(freq * ((data - mean)**2)) / np.sum(freq)


def mean_var(data, freq, shephard=False, binwidth=None):
    # returns tuple of mean and varience
    mean = _mean(data, freq)
    var = _var(data, freq, mean=mean)
    if ((shephard is True) and (binwidth is not None)):
        # apply shephard correction
        var = var - binwidth**2 / 12
    return mean, var


def filter(energy, freq, cutoff=0.006):
    # filter out low energy tail
    maxEnergy = np.amax(freq)  # energy of maximum
    mask = freq > cutoff * maxEnergy
    meanBackground = np.mean( ~mask * freq)
    freq -= 50*meanBackground
    freq *= freq > 0    # remove negative values
    return freq

# Loop over every energy & thickness
# for e in [0.250,]:
#    for t in [5.,]:
# for e, t in [(0.230, 3.), (0.230, 5.)]
for e in energies:
    for t in thickness:
        # set the directory
        dir = "/{rThickness}-{bEnergy:03}/".format(rThickness=round(t), bEnergy=round(1000*e))

        # Read uprange data
        freqUprange, energy, binWidth, areaUprange = read_data("in001_fort.27", directory=dir, normalization='auto')

        # Read downrange data
        freqDownrange, energy, binWidth, areaDownrange = read_data("in001_fort.28", directory=dir, normalization=1/areaUprange)  # normalise downrange to uprange area

        # Apply filter to downrange frequency data to remove low energy tail
        filteredFreqDownrange = filter(energy, np.copy(freqDownrange))

        # Calculate mean & varience of data
        meanUprange, varUprange = mean_var(energy, freqUprange, shephard=True, binwidth=binWidth)
        meanDownrange, varDownrange = mean_var(energy, filteredFreqDownrange, shephard=True, binwidth=binWidth)

        ratio = areaDownrange / areaUprange  # ratio of downrange protons to uprange protons

        # print some information
        print("E= {:.3f} GeV, x= {:.3f} cm".format(e, t))      # Energy and thickness
        print(" === Before normalization === ")
        print("Uprange area: {}".format(areaUprange))
        print("Downrange area: {}".format(areaDownrange))
        print("ratio: {}".format(ratio)) # first should be 0.9912132364763618

        nareaUprange = rectangular(freqUprange, dx=binWidth)
        nareaDownrange = rectangular(freqDownrange, dx=binWidth)
        print("E= {:.3f} GeV, x= {:.3f} cm".format(e, t))      # Energy and thickness
        print(" === Before normalization === ")
        print("Uprange area: {}".format(areaUprange))
        print("Downrange area: {}".format(areaDownrange))
        print("ratio: {}".format(ratio)) # first should be 0.9912132364763618
        print(" === After normalization === ")
        print("Uprange area: {}".format(nareaUprange))           # should be 1.0s
        print("Downrange area: {}".format(nareaDownrange))       # should be ⪅ 1.0
        print("ratio: {}".format(nareaDownrange / nareaUprange)) # should be same as before
        print(" === Mean and Stanard Deviation === ")
        print("Uprange mean: {}\nUprange varience: {}".format(meanUprange, varUprange))
        print("Downrange mean: {}\nDownrange varience: {}".format(meanDownrange, varDownrange))
        print("\n\n\n")

        if plotting:
            # Plot the data
            plt.bar(x=energy, height=freqUprange,   width=binWidth, color=(0.4,0.4,1))      # Uprange
            plt.bar(x=energy, height=freqDownrange, width=binWidth, color=(1,0.1,0.1,0.6))  # Downrange

            # Plot the reconstructed gaussian for the uprange proton energy distribution
            yDown = ratio * gaussian(meanDownrange, std=np.sqrt(varDownrange))(energy)
            yUp = gaussian(meanUprange, std=np.sqrt(varUprange))(energy)

            plt.plot(energy, yDown)
            plt.plot(energy, yUp)

            # Annotations
            plt.xlabel("Kinetic Energy (MeV)")
            plt.ylabel("Probability Density of Proton Kinetic Energy")
            plt.title("E= {:.3f} GeV, x= {:.3f} cm".format(e, t))
            plt.xlim(meanDownrange - 10 * np.sqrt(varDownrange), meanUprange + 10 * np.sqrt(varDownrange))

            plt.show()



        pandEnergy.append(e)
        pandThickness.append(t)
        pandMeanUprange.append(meanUprange)
        pandStdUprange.append(np.sqrt(varUprange))
        pandMeanDownrange.append(meanDownrange)
        pandStdDownrange.append(np.sqrt(varDownrange))
        pandRatio.append(ratio)


energyspecdata ={
    "Kinetic Energy (GeV)" : pandEnergy,
    "Thickness (cm)" : pandThickness,
    "Upstream Energy Mean (GeV)" : pandMeanUprange,
    "Downstream Energy Mean (GeV)" : pandMeanDownrange,
    "Upstream Energy Std" : pandStdUprange,
    "Downstream Energt Std" : pandStdDownrange,
    "Ratio" : pandRatio
}

if writecsv:
    df = pd.DataFrame(energyspecdata)
    print(df)
    df.to_csv("DownrangeEnergySpectra(FLUKA).csv")
