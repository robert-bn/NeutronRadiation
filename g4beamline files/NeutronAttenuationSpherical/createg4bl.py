from numpy import arange
import os

for detnum in arange(10,300,10):
    with open("template.txt", 'r') as templatef:
        os.makedirs(os.getcwd() + "/Det{num}/".format(num=detnum))
        with open(os.getcwd() + "/Det{num}/det.g4bl".format(num=detnum), 'w+') as f:
            for line in templatef:
                if line.startswith("sphere Target"):
                    line = line.replace("$outerRadius$",str(detnum))
                print(line, file=f, end='')
