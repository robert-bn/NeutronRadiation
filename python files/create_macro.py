from numpy import arange

def format_each(ene, sigma, n):
    print("/gps/ene/mono {} MeV".format(ene))
    print("/gps/ene/sigma {:.2f} MeV".format(sigma))
    print("/run/beamOn {}".format(n))
    print("")


print("/run/initialize")
print("/gps/pos/type Beam")
print("/gps/pos/sigma_r 5 mm")
print("")
print("/gps/ene/type Gauss")


for each in arange(70,260,10):
    format_each(each, 0.004*each, 10000000)
