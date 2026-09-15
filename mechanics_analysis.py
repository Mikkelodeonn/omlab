import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

class mechanics: 
    def __init__(self, measurement_type: str, thermal_freqs_in_Hz: str, ringdown_freqs_in_Hz: str, modes: list, date: str) -> None:
        match measurement_type:
            case "thermal":
                self.thermal_data = []

                for mode, freq in zip(modes, thermal_freqs_in_Hz): 
                    data = [np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\"+date+"\\"+mode+"\\Thermal PCS 02(1,1), "+freq+"Hz,100Ave, RBW0_1Hz,900_7nm_170mbar_0Vdc_"+str(i)+".txt", skiprows=1) for i in range(1,6)]

                    self.thermal_data.append(data)

            case "ringdown":
                self.ringdown_data = []

                for mode, freq in zip(modes, ringdown_freqs_in_Hz):
                    data = [np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\"+date+"\\"+mode+"\\Ringdown ChamberPressure = 2-8e-4(1,1), "+freq+"Hz, 100Ave, RBW114Hz, 910-685nm_1-2e-05mbar_90Vdc_"+str(i)+".txt", skiprows=1) for i in range(1,6)]

                    self.ringdown_data.append(data)

            case "both":
                self.thermal_data = []
                self.ringdown_data = []

                for mode, freq1, freq2 in zip(modes, thermal_freqs_in_Hz, ringdown_freqs_in_Hz): 
                    data1 = [np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\"+date+"\\"+mode+"\\Thermal PCS 02(1,1), "+freq1+"Hz,100Ave, RBW0_1Hz,900_7nm_170mbar_0Vdc_"+str(i)+".txt", skiprows=1) for i in range(1,6)]

                    data2 = [np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\"+date+"\\"+mode+"\\Ringdown ChamberPressure = 2-8e-4(1,1), "+freq2+"Hz, 100Ave, RBW114Hz, 910-685nm_1-2e-05mbar_90Vdc_"+str(i)+".txt", skiprows=1) for i in range(1,6)]

                    self.thermal_data.append(data1)
                    self.ringdown_data.append(data2)

    def ringdown_fit(self):
        print(self.thermal_data[0][0][:,0])


modes = ["1,1", "1,2", "2,1", "2,2", "2,3", "3,2", "3,3", "1,4", "4,1", "2,4", "3,4", "1,5", "5,1"]
thermal_freqs = ["195024", "308127", "308540", "390010", "496938", "497416", "585000", "567926", "569047", "616148", "689598", "702346", "703814"]
ringdown_freqs = ["195024", "308131", "308542", "390011", "496940", "497400", "585017", "567924", "569053", "616147", "689600", "702349", "703816"]

D1 = mechanics(measurement_type="both", 
               thermal_freqs_in_Hz = thermal_freqs, 
               ringdown_freqs_in_Hz = ringdown_freqs,
               modes = modes, 
               date = "20260909")

D1.ringdown_fit()