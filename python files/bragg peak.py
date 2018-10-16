# -*- coding: utf-8 -*-
"""
Code to numerically integrate the Bethe-Bloch formula and plot the bragg peak
"""
import material as mat
import numpy as np
# from scipy.integrate import quadrature
import matplotlib.pyplot as plt
from scipy.constants import e, electron_mass, proton_mass, pi, epsilon_0, Avogadro,c

eV = e
MeV = 10e6 * eV


def bethe(E, material):
    return -((e**2 / (4*pi*epsilon_0) ) ** 2 * (2*pi*material.Z*material.rho*
           Avogadro*proton_mass * 10e4 /(material.A*electron_mass*E)) *
    np.log(4*electron_mass*E/(material.I*proton_mass)))


def gaussian(n, sigma):
    x = np.linspace(-3*sigma,3*sigma,n)
    return  np.exp(-(x/sigma)**2/2)

"""
def v2(kinetic, mass):
    energy = kinetic + mass*c**2
    return energy, c **2 * (1 - mass**2 * c**4 / energy**2)


def bethe(E, material):
    return -((e**2 / (4*pi*epsilon_0) ) ** 2 * (4*pi*material.Z*material.rho*
           Avogadro*proton_mass * 10e4 /(material.A*electron_mass*v2(E, proton_mass))) *
    np.log(2*electron_mass*v2(E, proton_mass)/(material.I*proton_mass)))
"""

n = 6000
xrange = 0.6
x = np.linspace(0,xrange,n)
DE = np.empty_like(x)
Eb = np.empty_like(x)
deltax = xrange/n
E_0 = 250 * MeV
E = E_0


for i in range(n):
    if E > 0:#
        E += bethe(E, mat.water) * deltax
        DE[i] = bethe(E, mat.water)
    else:
        DE[i] = 0
    Eb[i] = E



plt.plot(x, -DE)
plt.show()