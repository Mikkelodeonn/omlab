from KIM101_motion_controller import kim101
from Picomotor_motion_controller import picomotor
from keysight_scope_controller import keysight_scope
from scipy.optimize import curve_fit

import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf
import time

class guitar:
    def __init__(self, x_stage_serial: str, y_stage_serial: str, scope_visa_address: str, x_channel=1, y_channel=2, sim=False):
        self.x_stage = kim101(serial=x_stage_serial, channel=x_channel, sim=sim)
        self.y_stage = kim101(serial=y_stage_serial, channel=y_channel, sim=sim)
        self.scope = keysight_scope(visa_address=scope_visa_address)
        self.z_stage = picomotor()


    def fit_func(self, x, A, sigma, top_width, x0, bg): 
        f1 = erf((x - x0 + top_width/2) / (np.sqrt(2) * sigma))
        f2 = erf((x - x0 - top_width/2) / (np.sqrt(2) * sigma))
        f3 = 2 * erf(top_width / (2 * np.sqrt(2) * sigma))
        return A * ((f1 - f2) / f3) + bg
    
    def center_on_guitar(self, max_step: int, stepsize: int, scope_channel: int):

        range = np.arange(-max_step, max_step+stepsize, stepsize)

        init_fit_params = [1, 1, 100, 0, 1]

        x_vals = []
        y_vals = []

        self.x_stage.Zero()
        self.y_stage.Zero()
        time.sleep(1)

        for x in range:
            self.x_stage.MoveTo(int(x))
            time.sleep(1)
            val = self.scope.average_voltage(channel=scope_channel)
            print(val)
            x_vals.append(val)

        popt_x, pcov_x = curve_fit(self.fit_func, range, x_vals, p0=init_fit_params)
        time.sleep(5)

        self.x_stage.MoveTo(int(popt_x[3]))
        #self.x_stage.MoveTo(7)

        for y in range:
            self.y_stage.MoveTo(int(y))
            time.sleep(1)
            val = self.scope.average_voltage(channel=scope_channel)
            print(val)
            y_vals.append(val)

        popt_y, pcov_y = curve_fit(self.fit_func, range, y_vals, p0=init_fit_params)
        time.sleep(5)

        self.y_stage.MoveTo(int(popt_y[3]))
        #self.y_stage.MoveTo(12)
        print("Found center = (" + str(int(popt_x[3])) + ", " + str(int(popt_y[3])) + ")")
        print("Found width (x): " + str(popt_x[4]))
        print("Found width (y): " + str(popt_y[4]))
        return [popt_x[3], popt_y[3], popt_x[4], popt_y[4]] ## [x_pos, y_pos, x_width, y_width]
    
    def locate_beam_focus(self, max_steps: int, stepsize: int, scope_channel: int):
        self.z_stage.zero()

        optimal_width = self.center_on_guitar(max_steps=max_steps, 
                                      stepsize=stepsize, 
                                      scope_channel=scope_channel)[2]

        while True:
            self.z_stage.MoveBy(10)
            width = self.center_on_guitar(max_steps=max_steps, 
                                              stepsize=stepsize, 
                                              scope_channel=scope_channel)[2]
            if width > optimal_width:
                optimal_width = width
            else:
                self.z_stage.MoveBy(-10)
                break
        
        while True:
            self.z_stage.MoveBy(-10)
            width = self.center_on_guitar(max_steps=max_steps, 
                                              stepsize=stepsize, 
                                              scope_channel=scope_channel)[2]
            if width > optimal_width:
                optimal_width = width
            else:
                self.z_stage.MoveBy(10)
                break

        print("Sample is in focus!")
        

            


G1 = guitar(x_stage_serial="97000001", 
            y_stage_serial="97000002", 
            scope_visa_address="USB0::0x0957::0x1796::MY53100155::0::INSTR",
            sim=False)

#G1.center_on_guitar(max_step=20, 
#                    stepsize=5, 
#                    scope_channel=1)


## Test implementation in the lab. Remove 50/50 BS and try to align with the script. Debug as you go.

