# A waste of time

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import dblquad

mu = 0.01376169  # neutron attenuation cooefficient (/mm)
lamda = 1/mu     # neutron mean free path
d = 100          # thickness of shell (mm)
R = 200          # outer radius of sphere, i.e. inner radius + d (mm)
theta0 = np.arcsin(np.sqrt(lamda/d))
# calculated from MC simulation for

def f(x, th):
    return np.exp(-th**2 / (2 * np.arctan2( np.sqrt(lamda)**2, np.sqrt(x*np.abs(np.cos(x))) ) **2 ) )

def integrand_u(x, th):
    return np.sin(th) * np.exp(-mu*x) * f(th, x)

def integrand_d(x, th):
    return np.sin(th) * f(th, x)

def x_min(th):
    return 0

def x_max(th):
    return -(R - d)*np.cos(th) + np.sqrt((R-d)**2 * np.cos(th)**2 + 2*R*d -d**2)

intu = dblquad(integrand_u, 0, np.pi, x_min, x_max)
intd = dblquad(integrand_d, 0, np.pi, x_min, x_max)

print(intu)
print(intd)

print(intu[0]/intd[0])

th = np.linspace(-2*np.pi, 2*np.pi)
plt.plot(th, f(2, th))
plt.show()
