import os

energies = [0.250,0.230,0.200,0.150,0.100,0.07]  # MeV
spread   = [0.1020,0.0979,0.0913,0.0790,0.0645,0.0540]
thickness = [1.,2.,3.,5.]   # cm

for i, e in enumerate(energies):
    for t in thickness:
        with open("template.txt", 'r') as templatef:
            directory = "/{rThickness}-{bEnergy}/".format(rThickness=t, bEnergy=e)
            os.makedirs(os.getcwd() + directory)
            with open(os.getcwd() + directory + "in.inp", 'w+') as f:
                for line in templatef:
                    line = line.replace("$rThickness$",str(t))
                    line = line.replace("$bEnergy$",str(e))
                    line = line.replace("$bEnergySpread$",str(spread[i]))
                    print(line, file=f, end='')
