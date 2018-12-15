from numpy import arange, rint

def format_each(ene, sigma, n):
    print("/gps/ene/mono {} MeV".format(ene))
    print("/gps/ene/sigma {:.2f} MeV".format(sigma))
    print("/run/beamOn {}".format(n))
    print("")


print("/run/initialize")
print("/gps/pos/type Beam")
print("")
print("/gps/ene/type Gauss")

def num(e):
    # Calibrated to water activation C11
    # DONT USE TO MAKE MACRO FOR RANGESHIFTER. USE CONSTANT NUMBER FOR RANGESHIFTER
    return -0.05*(e/10) + 1.4

for each in arange(70,260,10):
    format_each(each, 0.004*each, rint(20000000*num(each)))
