import numpy as np  
import matplotlib.pyplot as plt

data2 = np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\20260227\\Thermal PCS 02(1,1), 1057727Hz,80Ave, RBW0_1Hz,900_7nm_170mbar_0Vdc, 27-Feb-2026 07-56-13.txt", skiprows=1)

data1 = np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\20260227\\Thermal PCS 02(1,1), 1057727Hz,80Ave, RBW0_1Hz,900_7nm_170mbar_0Vdc, 27-Feb-2026 08-08-49.txt", skiprows=1)

freq = data1[:, 0] 
dB = data1[:, 1] 
bin_size = 1

freq = [np.average(freq[i:i+bin_size]) for i in range(0, len(freq)-bin_size, bin_size)]
dB = [np.average(dB[i:i+bin_size]) for i in range(0, len(dB)-bin_size, bin_size)]

fig, ax = plt.subplots(2, 1, figsize=(15, 6))

ax[0].plot(freq, dB, label='Thermal PCS 02(1,1), 1057727Hz,80Ave, RBW0_1Hz,900_7nm_170mbar_0Vdc')
ax[0].set_xlabel('Frequency (kHz)')   
ax[0].set_ylabel('Power (dB)')
ax[0].grid()
#ax[0].legend()

freq2 = data2[:, 0] 
dB2 = data2[:, 1] 
bin_size = 1

freq2 = [np.average(freq2[i:i+bin_size]) for i in range(0, len(freq2)-bin_size, bin_size)]
dB2 = [np.average(dB2[i:i+bin_size]) for i in range(0, len(dB2)-bin_size, bin_size)]

ax[1].plot(freq2, dB2, label='Thermal PCS 02(1,1), 1057727Hz,80Ave, RBW0_1Hz,900_7nm_170mbar_0Vdc')
ax[1].set_xlabel('Frequency (kHz)')   
ax[1].set_ylabel('Power (dB)')
ax[1].grid()
#ax[1].legend()
plt.show()