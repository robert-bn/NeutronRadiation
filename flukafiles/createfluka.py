from numpy import arange
import os

energies = [0.250,0.230,0.200,0.150,0.100,0.70]  # MeV
thickness = [1.,2.,3.,5.]   # cm

for e in energies:
    for t in thickness
        with open("template.txt", 'r') as templatef:
            directory = /t{rThickness}e{bEnergy}/".format(rThickness=t, bEnergy=e)
            os.makedirs(os.getcwd() + directory)
            with open(os.getcwd() + directory, 'w+') as f:
                for line in templatef:
                    line = line.replace("$rThickness$",str(t))
                    line = line.replace("$bEnergy$",str(e))
                    print(line, file=f, end='')
