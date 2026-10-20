import numpy as np
import matplotlib.pyplot as plt

C1_thermal_freqs = ["50611", "102356", "133764", "153941", "161409", "179346", "185577", "202699", "210000", "220953", "231175", "235865", "237469", "280731", "286268", "288697", "289651"]
#C1_thermal_freqs = ["50613", "102367", "133774", "153966", "161420", "202748", "210597", "220974", "231196", "280749", "286289", "288723", "289673", "340004", "340647", "341277", "341958", "346480", "396423", "414669"]
C2_freqs = ["51361", "102761", "102861", "136491", "161453", "162390", "185719", "185802", "221775", "236551", "237177", "276701", "286507", "289481", "342035", "342765", "343007"]

sim_data = np.loadtxt(r"C:\\Users\\au601136\\omlab\\mechanics\\450Pad_300-800MPa-modes.txt", skiprows=5)

freqs = [float(x)*1e-3 for x in C2_freqs]
sim1 = sim_data[0][2:]
sim2 = sim_data[1][2:]

membrane_freqs = []

for n in range(5):
    for m in range(5):
        freq = freqs[0]*np.sqrt((n+1)**2 + (m+1)**2) / np.sqrt(2)
        membrane_freqs.append(freq)

membrane_freqs = np.sort(membrane_freqs)

plt.figure(figsize=(10,6))
plt.plot(freqs, "o", label="C2 data")
plt.plot(membrane_freqs, "o", color="magenta", label="membrane (analytical)")
plt.plot(sim2, "o", label="800 MPa sim")
plt.xlabel("mode number", fontsize=20)
plt.ylabel("frequency [kHz]", fontsize=20)
plt.legend()
plt.grid(alpha=0.5)
plt.show()
