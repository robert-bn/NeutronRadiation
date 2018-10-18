from numpy import arange
import os

sphere_radius = 5000

for detnum in arange(10,300,10):
    with open("template.txt", 'r') as templatef:
        os.makedirs(os.getcwd() + "/Det{num}/".format(num=detnum))
        with open(os.getcwd() + "/Det{num}/det.g4bl".format(num=detnum), 'w+') as f:
            for line in templatef:
                line = line.replace("$detNum$",str(detnum))
                line = line.replace("$outerRadius$",str(sphere_radius + detnum))
                line = line.replace("$innerRadius$",str(sphere_radius))
                print(line, file=f, end='')
