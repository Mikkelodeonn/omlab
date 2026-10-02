import numpy as np
import matplotlib.pyplot as plt

C1_thermal_freqs = ["50611", "102356", "133764", "153941", "161409", "179346", "185577", "202699", "210000", "220953", "231175", "235865", "237469", "280731", "286268", "288697", "289651"]
#C1_thermal_freqs = ["50613", "102367", "133774", "153966", "161420", "202748", "210597", "220974", "231196", "280749", "286289", "288723", "289673", "340004", "340647", "341277", "341958", "346480", "396423", "414669"]


sim_data = np.loadtxt(r"C:\\Users\\au601136\\omlab\\mechanics\\20260929\\450Pad_300-800MPa-modes.txt", skiprows=5)

freqs = [float(x)*1e-3 for x in C1_thermal_freqs]
sim1 = sim_data[0][2:]
sim2 = sim_data[1][2:]

plt.figure(figsize=(10,6))
plt.plot(freqs, "o", label="C1 data")
#plt.plot(sim1, "o", label="300 MPa sim")
plt.plot(sim2, "o", label="800 MPa sim")
plt.xlabel("mode number", fontsize=20)
plt.ylabel("frequency [kHz]", fontsize=20)
plt.legend()
plt.grid(alpha=0.5)
plt.show()
