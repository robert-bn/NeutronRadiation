# A waste of time

import numpy as np
from scipy.integrate import dblquad

mu = 0.01376169  # neutron attenuation cooefficient (/mm)
lamda = 1/mu     # neutron mean free path
d = 100          # thickness of shell (mm)
R = 100          # outer radius of sphere, i.e. inner radius + d (mm)
theta0 = np.arcsin(np.sqrt(lamda/d))
# calculated from MC simulation for

def f(x, th):
    # return np.exp(th**2 / (2 * np.arcsin(lamda /( x * np.cos(th) ))))
    if th < theta0:
        return 1.
    else:
        return 0.

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
