import numpy as np
import material as mat
from scipy.integrate import quadrature
from scipy.constants import e, electron_mass, proton_mass, pi, epsilon_0, Avogadro
# import matplotlib.pyplot as plt

eV = e
MeV = 10e6 * eV


def bethe(E, material):
    return -1/((e**2 / (4*pi*epsilon_0) ) ** 2 * (2*pi*material.Z*material.rho*
           Avogadro*proton_mass * 10e4 /(material.A*electron_mass*E)) * np.log(4*electron_mass*E/(material.I*proton_mass)))


def R(E, material):
    return quadrature(bethe, E, 0, args=material)


    
print(R(250*MeV, mat.air))

"""

energy = 10**np.linspace(-3,3,100)
r = np.empty_like(energy)

for i in range(len(energy)):
    r[i] = R(energy[i] * MeV, water)

plt.loglog(energy, r )
plt.show()
"""