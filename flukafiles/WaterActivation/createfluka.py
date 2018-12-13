import os
from numpy import sqrt
import pandas as pd

energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # GeV
# spread   = [0.1020,0.0979,0.0913,0.0790,0.0645,0.0540]
bins = [0.30,0.28,0.25,0.20,0.15,0.12]
bins2 = [0.17,0.15,0.12,0.06,0.00,0.00]
thickness = [1.,2.,3.,5.0]   # cm

cdownstreamEnergy, cdownstreamError, cenergy, cthickness = 'Downstream Energy Mean (GeV)', 'Downstream Energt Std','Kinetic Energy (GeV)', 'Thickness (cm)'

m_p = .938  # GeV

with open("DownrangeEnergySpectra(FLUKA).csv") as downrangef:
    df = pd.read_csv("DownrangeEnergySpectra(FLUKA).csv")
    downstreamE = df["Downstream Energy Mean (GeV)"]
    downstreamError = df["Downstream Energt Std"]


def spread(T, δ=0.004):
    # returns energy spread in GeV
    E = T + m_p
    return 2.335 *  δ * T * E / sqrt(E**2 - m_p**2)

def FWHM(T, dT):
    # returns energy spread in GeV
    E = T + m_p
    return float(2.335 * dT * E / sqrt(E**2 - m_p**2))



def create_files():
    for i, e in enumerate(energies):
        for t in thickness:
            print(df[(df[cthickness] == t) & (df[cenergy] == e)][cdownstreamEnergy].values)
       
            with open("template.txt", 'r') as templatef:
                directory = "/{rThickness}-{bEnergy:03}/".format(rThickness=round(t), bEnergy=round(1000*e))
                os.makedirs(os.getcwd() + directory)
                with open(os.getcwd() + directory + "in.inp", 'w+') as f:
                    
                    downe = float(df[(df[cthickness] == t) & (df[cenergy] == e)][cdownstreamEnergy].values)
                    downerr = float(df[(df[cthickness] == t) & (df[cenergy] == e)][cdownstreamError].values)
                    downFWHM = FWHM(T=downe, dT=downerr)

                    for line in templatef:
                        line = line.replace("$rThickness$",str(t))
                        line = line.replace("$cBins$","{:.2f}").format(bins2[i])
                        line = line.replace("$bBins$","{:.2f}".format(bins[i]))
                        line = line.replace("$aEnergy$","{:.2f}".format(e))
                        line = line.replace("$aThickness$",str(t))
                        
                        line = line.replace("$bEnergy$","{:.6f}".format(downe))
                        line = line.replace("$bEnergySpread$","{:.6f}".format(downFWHM))
                        print(line,file=f, end='')

create_files()
