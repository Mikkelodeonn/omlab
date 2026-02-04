import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

xdata = np.loadtxt("C:\\Users\\au601136\\omlab\\beam waist\\bwx_75_200_65_inside_chamber_3.txt", skiprows=1)
ydata = np.loadtxt("C:\\Users\\au601136\\omlab\\beam waist\\bwy_75_200_65_inside_chamber_3.txt", skiprows=1)

def gaussian(x, a, x0, sigma, offset):
    return a * np.exp(-(x - x0)**2 / (2 * sigma**2)) + offset

# Fit the data to the Gaussian function
popt_x, pcov_x = curve_fit(gaussian, xdata[:, 0], xdata[:, 1], p0=[200, 8, 1, 0], maxfev=10000)
popt_y, pcov_y = curve_fit(gaussian, ydata[:, 0 ], ydata[:, 1], p0=[200, 8, 1, 0], maxfev=10000)      

# Extract fitted parameters
a_x, x0_x, sigma_x, offset_x = popt_x
a_y, x0_y, sigma_y, offset_y = popt_y   

# Generate fitted data for plotting
x_fit = np.linspace(min(xdata[:, 0]), max(xdata[:, 0]), 100)
y_fit_x = gaussian(x_fit, *popt_x)  
y_fit_y = gaussian(x_fit, *popt_y)  

# Plot the data and the fits

print(f"Fitted parameters for x direction: a={a_x}, x0={x0_x}, sigma={sigma_x}, offset={offset_x}")
print(f"Fitted parameters for y direction: a={a_y}, x0={x0_y}, sigma={sigma_y}, offset={offset_y}")

plt.figure(figsize=(12, 6))     

plt.subplot(1, 2, 1)
plt.scatter(xdata[:, 0], xdata[:, 1], label='$w_0 \\approx$ %s μm' % str(round(np.abs(5.2*2*sigma_x),2)), color='blue') 
plt.plot(x_fit, y_fit_x, label='Fit', color='red')        
plt.title('Beam Waist Fit - x Direction')
plt.xlabel('Position (mm)')
plt.ylabel('Intensity (a.u.)')
plt.legend()
plt.grid()
plt.subplot(1, 2, 2)
plt.scatter(ydata[:, 0], ydata[:, 1], label='$w_0 \\approx$ %s μm' % str(round(np.abs(5.2*2*sigma_y),2)), color='green') 
plt.plot(x_fit, y_fit_y, label='Fit', color='orange') 
plt.title('Beam Waist Fit - y Direction')
plt.xlabel('Position (mm)')
plt.ylabel('Intensity (a.u.)')
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

