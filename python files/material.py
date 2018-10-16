from scipy.constants import Avogadro, e

class Material:
    def __init__(self, I, A, Z, rho):
        self.I = I
        self.A = A
        self.Z = Z
        self.rho = rho
        self.n = Avogadro * Z * rho / (A * 0.0001)
    
    def __str__(self):
        return "I = {} J\nZ = {}\nA = {}\nρ = {} kg m⁻³\nn = {} m⁻³".format(self.I, self.A, self.Z, self.rho, self.n)

water = Material(75*e, 18, 8, 1000)
air = Material(85*e, 0.2*16 + 0.8*14, 0.2*8+0.8*7, 1.225)