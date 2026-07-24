from KIM101_motion_controller import kim101
from Picomotor_motion_controller import picomotor
from keysight_scope_controller import keysight_scope
from scipy.optimize import curve_fit

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
import time
import matplotlib.pyplot as plt

class guitar:
    def __init__(self, stage_serial: str, scope_visa_address: str, sim=False):
        self.xy_stage = kim101(serial=stage_serial, sim=sim)
        self.scope = keysight_scope(visa_address=scope_visa_address)
        self.z_stage = picomotor(auto_detect=True)


    def fit_func(self, x, A, sigma, x0, w, bg): 
        f1 = erf((x - x0 + w / 2) / (np.sqrt(2) * sigma))
        f2 = erf((x - x0 - w / 2) / (np.sqrt(2) * sigma))
        f3 = 2 * erf(w / (2 * np.sqrt(2) * sigma))
        return A * (f1 - f2) / f3 + bg
    
    def center_on_guitar(self, scan_length: int, stepsize: int, scope_channel: int):

        init_fit_params = [17, 50, 200, 250, 1]

        previous_xval = np.inf

        while True: 
            val = self.scope.average_voltage(channel=scope_channel)
            self.xy_stage.MoveBy(-stepsize, 1)

            if val < 1 and np.abs(val - previous_xval) < 0.1:
                break

            previous_xval = val

        init_xpos = self.xy_stage.GetPosition(channel=1)
        
        x_vals = []

        xpos = [init_xpos]

        while True:
            val = self.scope.average_voltage(channel=scope_channel)
            x_vals.append(val)
            print(xpos[-1]-init_xpos, "->", val)
            if np.abs(init_xpos - self.xy_stage.GetPosition(channel=1)) > scan_length:
                break
            self.xy_stage.MoveBy(steps=stepsize, channel=1)
            new_xpos = self.xy_stage.GetPosition(channel=1)
            xpos.append(new_xpos)
            time.sleep(2)

        x_fit = np.array(xpos) - xpos[0]

        popt_x, pcov_x = curve_fit(self.fit_func, x_fit, x_vals, p0=init_fit_params, maxfev=1000000)
        [Ax, sigmax, x0, wx, bgx] = popt_x
        print("x0 = ", x0)
        time.sleep(5)

        while True: 
            val = self.scope.average_voltage(channel=scope_channel)
            self.xy_stage.MoveBy(-stepsize, 1)

            if val > 1 and np.abs(val - previous_xval) < 0.1:
                break

            previous_xval = val
    
        while True: 
            val = self.scope.average_voltage(channel=scope_channel)
            self.xy_stage.MoveBy(-stepsize, 1)

            if val < 1 and np.abs(val - previous_xval) < 0.1:
                break

            previous_xval = val

        self.xy_stage.MoveBy(int(x0), 1)
        time.sleep(5)

        previous_yval = np.inf

        while True:
            val = self.scope.average_voltage(channel=scope_channel)
            self.xy_stage.MoveBy(-stepsize, 2)

            if val < 1 and np.abs(val - previous_yval) < 0.1:
                break

            previous_yval = val

        init_ypos = self.xy_stage.GetPosition(channel=2)
        
        y_vals = []

        ypos = [init_ypos]

        while True:
            val = self.scope.average_voltage(channel=scope_channel)
            y_vals.append(val)
            print(ypos[-1] - init_ypos, "->", val)
            if np.abs(init_ypos - self.xy_stage.GetPosition(channel=2)) > scan_length:
                break
            self.xy_stage.MoveBy(steps=stepsize, channel=2)
            new_ypos = self.xy_stage.GetPosition(channel=2)
            ypos.append(new_ypos)
            time.sleep(2)

        y_fit = np.array(ypos) - ypos[0]

        popt_y, pcov_y = curve_fit(self.fit_func, y_fit, y_vals, p0=init_fit_params, maxfev=1000000)
        [Ay, sigmay, y0, wy, bgy] = popt_y
        print("y0 = ", y0)
        time.sleep(5)

        while True: 
            val = self.scope.average_voltage(channel=scope_channel)
            self.xy_stage.MoveBy(-stepsize, 2)

            if val > 1 and np.abs(val - previous_yval) < 0.1:
                break

            previous_yval = val
    
        while True: 
            val = self.scope.average_voltage(channel=scope_channel)
            self.xy_stage.MoveBy(-stepsize, 2)

            if val < 1 and np.abs(val - previous_yval) < 0.1:
                break

            previous_yval = val

        self.xy_stage.MoveBy(int(y0), 2)
        time.sleep(5)

        print("Found center (x, y) = (" + str(int(x0)) + ", " + str(int(y0)) + ")")
        print("Found width (x): " + str(wx))
        print("Found width (y): " + str(wy))

        x_plot = np.linspace(x_fit[0], x_fit[-1], 1000)
        y_plot = np.linspace(y_fit[0], y_fit[-1], 1000)

        fig, ax = plt.subplots(1,2, figsize=(14,4))
        ax[0].scatter(x_fit, x_vals, label="x data", color="firebrick")
        ax[1].scatter(y_fit, y_vals, label="y data", color="royalblue")
        ax[0].plot(x_plot, self.fit_func(x_plot, *popt_x), label="x fit", color="firebrick", alpha=0.5)
        ax[1].plot(y_plot, self.fit_func(y_plot, *popt_y), label="y fit", color="royalblue", alpha=0.5)
        ax[0].set_xlabel("position [steps]") 
        ax[1].set_xlabel("position [steps]") 
        ax[0].set_ylabel("averaged signal [V]") 
        ax[1].set_ylabel("averaged signal [V]") 
        ax[0].legend(loc=1)
        ax[1].legend(loc=1)
        plt.show()

        return [x0, y0, wx, wy] ## [x-center, y-center, x-topwidth, y-topwidth]
    
    def locate_beam_focus(self, scan_length: int, xy_stepsize: int, scope_channel: int, z_stepsize: int):
        self.z_stage.zero()

        optimal_width = self.center_on_guitar(scan_length=scan_length, 
                                      stepsize=xy_stepsize, 
                                      scope_channel=scope_channel)[2]

        while True:
            print("Found width: ", optimal_width)
            self.z_stage.MoveBy(axis=1, steps=z_stepsize)
            width = self.center_on_guitar(scan_length=scan_length, 
                                              stepsize=xy_stepsize, 
                                              scope_channel=scope_channel)[2]
            if width > optimal_width:
                optimal_width = width
            else:
                self.z_stage.MoveBy(axis=1, steps=-z_stepsize)
                break
        
        while True:
            self.z_stage.MoveBy(axis=1, steps=-z_stepsize)
            width = self.center_on_guitar(scan_length=scan_length, 
                                              stepsize=xy_stepsize, 
                                              scope_channel=scope_channel)[2]
            if width > optimal_width:
                optimal_width = width
            else:
                self.z_stage.MoveBy(axis=1, steps=z_stepsize)
                break

        print("Sample is in focus!")
        

G1 = guitar(stage_serial="97251709", 
            scope_visa_address="USB0::0x0957::0x1796::MY57153094::0::INSTR",
            sim=False)

G1.center_on_guitar(scan_length=800, 
                    stepsize=20, 
                    scope_channel=1)

#G1.locate_beam_focus(scan_length=800,
#                     xy_stepsize=20, 
#                     scope_channel=1,
#                     z_stepsize=200)


