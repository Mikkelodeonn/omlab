import numpy as np
import matplotlib.pyplot as plt

data = np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\20261014\\mode11\\Ringdown C 02(1,1), 237177Hz, 100Ave, RBW10Hz, 940-9nm_9e-07mbar_16Vdc, 14-10-2026_002.txt", skiprows=1)

time = data[:,0]
signal = data[:,1]

plt.figure(figsize=(10,5))

plt.plot(time, signal, "o-")

plt.show()