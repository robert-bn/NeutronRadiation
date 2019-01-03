import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("DownrangeEnergySpectra.csv")

thicknesses = [1,2,3,5]

df["Kinetic Energy"]  *= 1e3
df["Downstream Energy Mean"] *= 1e3
df["Downstream Energy Std"] *= 1e3

fig, ax = plt.subplots()

for t in thicknesses:
    df_t = df[df["Thickness"]==t]
    df_t.plot(x="Kinetic Energy", y="Downstream Energy Mean", ax=ax)
    ax.fill_between(
        df_t["Kinetic Energy"],
        df_t["Downstream Energy Mean"] - df_t["Downstream Energy Std"],
        df_t["Downstream Energy Mean"] + df_t["Downstream Energy Std"],
        alpha=0.5
    )
ax.set_xticks(np.arange(70,250,5), minor=True)
ax.set_yticks(np.arange(0,250,5), minor=True)
ax.grid(True, which="major")
ax.grid(True, which="minor", alpha=0.4)
ax.set_xlim([70,250])
ax.set_ylim(bottom=0, top=250)
ax.legend(["{} cm range shifter".format(t) for t in thicknesses])

plt.xlabel("Input mean kinetic energy of protons (MeV)")
plt.ylabel("Output mean kinetic energy of protons (MeV)")
plt.show()
