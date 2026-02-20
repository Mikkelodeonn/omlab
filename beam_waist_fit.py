import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

xdata = np.loadtxt("C:\\Users\\au601136\\omlab\\beam waist\\bwx_75_200_65_inside_chamber_3.txt", skiprows=1)
ydata = np.loadtxt("C:\\Users\\au601136\\omlab\\beam waist\\bwy_75_200_65_inside_chamber_3.txt", skiprows=1)

def gaussian(x, A, sigma, B, x0):
    return A * np.exp(-((x-x0)**2)/(2*sigma**2)) + B

# Fit the data to the Gaussian function
popt_x, pcov_x = curve_fit(gaussian, xdata[:, 0], xdata[:, 1], p0=[200, 2, 1, 8], maxfev=10000)
popt_y, pcov_y = curve_fit(gaussian, ydata[:, 0 ], ydata[:, 1], p0=[200, 2, 1, 8], maxfev=10000)      

# Extract fitted parameters
#a_x, x0_x, sigma_x, offset_x = popt_x
#a_y, x0_y, sigma_y, offset_y = popt_y   

# Generate fitted data for plotting
x_fit = np.linspace(min(xdata[:, 0]), max(xdata[:, 0]), 1000)
y_fit_x = gaussian(x_fit, *popt_x)  
y_fit_y = gaussian(x_fit, *popt_y)  

# Plot the data and the fits

#print(f"Fitted parameters for x direction: a={a_x}, x0={x0_x}, sigma={sigma_x}, offset={offset_x}")
#print(f"Fitted parameters for y direction: a={a_y}, x0={x0_y}, sigma={sigma_y}, offset={offset_y}")

plt.figure(figsize=(12, 6))     

plt.subplot(1, 2, 1)
plt.scatter(xdata[:, 0]*5.2, xdata[:, 1], label='data', color='darkblue') 
plt.plot(x_fit*5.2, y_fit_x, label='fit: $w_0 \\approx$ %s μm' % str(round(np.abs(2*5.2*popt_x[1]),2)), color='cornflowerblue')        
plt.title('Beam Waist Fit - x Direction')
plt.xlabel('Position (μm)')
plt.ylabel('Intensity (a.u.)')
plt.legend()
plt.grid()
plt.subplot(1, 2, 2)
plt.scatter(ydata[:, 0]*5.2, ydata[:, 1], label='data', color='darkred') 
plt.plot(x_fit*5.2, y_fit_y, label='fit: $w_0 \\approx$ %s μm' % str(round(np.abs(2*5.2*popt_y[1]),2)), color='lightcoral') 
plt.title('Beam Waist Fit - y Direction')
plt.xlabel('Position (μm)')
plt.ylabel('Intensity (a.u.)')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

