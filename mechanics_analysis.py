import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

class mechanics: 
    def __init__(self, measurement_type: str, thermal_freqs_in_Hz: str, ringdown_freqs_in_Hz: str, modes: list, date: str) -> None:
        match measurement_type:
            case "thermal":
                self.thermal_data = {}

                for mode, freq in zip(modes, thermal_freqs_in_Hz): 
                    data = [np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\"+date+"\\"+mode+"\\Thermal PCS 02(1,1), "+freq+"Hz,100Ave, RBW0_1Hz,900_7nm_170mbar_0Vdc_"+str(i)+".txt", skiprows=1) for i in range(1,6)]

                    self.thermal_data[mode] = data

            case "ringdown":
                self.ringdown_data = {}

                for mode, freq in zip(modes, ringdown_freqs_in_Hz):
                    data = [np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\"+date+"\\"+mode+"\\Ringdown ChamberPressure = 2-8e-4(1,1), "+freq+"Hz, 100Ave, RBW114Hz, 910-685nm_1-2e-05mbar_90Vdc_"+str(i)+".txt", skiprows=1) for i in range(1,6)]

                    self.ringdown_data[mode] = data

            case "both":
                self.thermal_data = {}
                self.ringdown_data = {}

                for mode, freq1, freq2 in zip(modes, thermal_freqs_in_Hz, ringdown_freqs_in_Hz): 
                    data1 = [np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\"+date+"\\"+mode+"\\Thermal PCS 02(1,1), "+freq1+"Hz,100Ave, RBW0_1Hz,900_7nm_170mbar_0Vdc_"+str(i)+".txt", skiprows=1) for i in range(1,6)]

                    data2 = [np.loadtxt("C:\\Users\\au601136\\omlab\\mechanics\\"+date+"\\"+mode+"\\Ringdown ChamberPressure = 2-8e-4(1,1), "+freq2+"Hz, 100Ave, RBW114Hz, 910-685nm_1-2e-05mbar_90Vdc_"+str(i)+".txt", skiprows=1) for i in range(1,6)]

                    self.thermal_data[mode] = data1
                    self.ringdown_data[mode] = data2

    def ringdown_Qs(self, modes: list, ringdown_frequencies: list, sample_name: str) -> dict:

        Qs_dict = {}

        for mode, freq in zip(modes, ringdown_frequencies):

            Qs = []

            for measurement in range(0,5):
                xdata = self.ringdown_data[mode][measurement][:,0] * 1e-3
                ydata = self.ringdown_data[mode][measurement][:,1]

                plt.figure(figsize=(15,5))
                plt.plot(xdata, ydata, "o", alpha=0.5, label="ringdown data")

                clicked_points = plt.ginput(2, timeout=-1, show_clicks=True)

                x1 = clicked_points[0][0]
                x2 = clicked_points[1][0]

                mask = (xdata >= x1) & (xdata <= x2)

                xfit = xdata[mask]
                yfit = ydata[mask]

                def ringdown_fit(t, m, B):
                    z = m*t + B 
                    return z

                popt, pcov = curve_fit(ringdown_fit, xfit, yfit)

                τ = -10 / (popt[0]*np.log(10)) # calculation from log (dBm) to linear
                Q = 2 * np.pi * float(freq) * τ
                Qs.append(Q)

                xs_fit = np.linspace(x1,x2,1000)
                ys_fit = ringdown_fit(xs_fit, *popt)

                plt.plot(xs_fit, ys_fit, "-", lw=3, color="firebrick", label="linear fit: Q ~ %s" % str(round(Q,2)))
                plt.xlabel("time [s]")
                plt.ylabel("Intensity [dBm]")
                plt.title(mode+" ringdown "+str(measurement))
                plt.legend()

                save_dir = "C:\\Users\\au601136\\omlab\\mechanics\\"+sample_name
                filename = os.path.join(save_dir, mode+" ringdown "+str(measurement)+".png")

                plt.savefig(filename, dpi=300, bbox_inches="tight")
                print(os.path.abspath(filename))

                #plt.show()

            Qs_dict[mode] = {"measurement": np.mean(Qs),
                             "error": np.std(Qs)
                            }

        return Qs_dict

    def thermal_Qs(self, modes: list, thermal_frequencies: list, sample_name: str) -> dict:
        
        Qs_dict = {}

        for mode, freq in zip(modes, thermal_frequencies):

            Qs = []

            for measurement in range(0,5):
                xdata = self.thermal_data[mode][measurement][:,0]
                ydata = 10**(self.thermal_data[mode][measurement][:,1]/10)

                fig, ax = plt.subplots(figsize=(15,5))
                ax.plot(xdata, ydata, "o", alpha=0.5, label="thermal data")

                clicked_points = plt.ginput(2, timeout=-1, show_clicks=True)

                x1 = clicked_points[0][0]
                x2 = clicked_points[1][0]

                mask = (xdata >= x1) & (xdata <= x2)

                xfit = xdata[mask]
                yfit = ydata[mask]

                def thermal_fit(x, x0, Γ, B, A):
                    S = A / ((x0 - x)**2 + (Γ/2)**2) + B
                    return S

                popt, pcov = curve_fit(thermal_fit, xfit, yfit, p0=[float(freq)*1e-3, 0.1, -120, 100e3], maxfev=10000)

                Γ = popt[1]
                Ω0 = popt[0]
                Q = Ω0 / Γ
                Qs.append(Q)

                xs_fit = np.linspace(x1,x2,100000)
                ys_fit = thermal_fit(xs_fit, *popt)

                ax.clear()

                ax.plot(xs_fit, ys_fit, "-", lw=3, color="firebrick", label="thermal fit: Q ~ %s" % str(round(Q,2)))
                ax.plot(xfit, yfit, "o", alpha=0.6, color="royalblue", label="data")
                ax.set_xlabel("frequency [kHz]")
                ax.set_ylabel("power [mW]")
                ax.set_title(mode+" thermal "+str(measurement))
                plt.legend()

                save_dir = "C:\\Users\\au601136\\omlab\\mechanics\\" + sample_name
                filename = os.path.join(save_dir, mode+" thermal "+str(measurement)+".png")

                plt.savefig(filename, dpi=300, bbox_inches="tight")
                print(os.path.abspath(filename))

                #plt.show()

            Qs_dict[mode] = {"measurement": np.mean(Qs),
                             "error": np.std(Qs)
                            }

        return Qs_dict

    def ringdown_plot(self, modes: list, ringdown_frequencies: list) -> None:
        Qs_dict = self.ringdown_Qs(modes, ringdown_frequencies) 

        Qs = [Qs_dict[mode]["measurement"] for mode in modes]
        Q_errors = [Qs_dict[mode]["error"] for mode in modes]
        frequencies = [int(freq) for freq in ringdown_frequencies]

        ys = np.linspace(0,max(Qs),1000)

        plt.figure(figsize=(15,5))
        plt.title("Ringdown")
        plt.errorbar(frequencies, Qs, yerr=Q_errors, color="firebrick", fmt="o", capsize=3, alpha=0.6)
        for frequency in frequencies:
            plt.plot([frequency]*len(ys), ys, "--", color="royalblue", alpha=0.4)
        plt.xlabel("frequency [Hz]")
        plt.ylabel("Q")
        #plt.legend()
        plt.show()


modes = ["1,1"]#, "1,2", "2,1", "2,2", "2,3", "3,2", "3,3", "1,4", "4,1", "2,4", "3,4", "1,5", "5,1"]
thermal_freqs = ["195024"]#, "308127", "308540", "390010", "496938", "497416", "585000", "567926", "569047", "616148", "689598", "702346", "703814"]
ringdown_freqs = ["195024"]#, "308131", "308542", "390011", "496940", "497400", "585017", "567924", "569053", "616147", "689600", "702349", "703816"]

D1 = mechanics(measurement_type="both", 
               thermal_freqs_in_Hz = thermal_freqs, 
               ringdown_freqs_in_Hz = ringdown_freqs,
               modes = modes, 
               date = "20260909")

#D1.ringdown_Qs(modes, ringdown_freqs, "D1")
D1.thermal_Qs(modes, thermal_freqs, "D1")
#D1.ringdown_plot(modes, ringdown_freqs, "D1")