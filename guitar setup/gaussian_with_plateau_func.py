import numpy as np
import matplotlib.pyplot as plt
from scipy.special import erf

# Parameters
#A -> Peak amplitude - bg
#sigma -> Gaussian sigma
#w -> Plateau width
#x0 -> Center
#bg -> background value

# x-axis
xs = np.linspace(-15, 20, 1000)

def flat_top(x, A, sigma, w, x0, bg): 
    f1 = erf((x - x0 + w/2) / (np.sqrt(2) * sigma))
    f2 = erf((x - x0 - w/2) / (np.sqrt(2) * sigma))
    f3 = 2 * erf(w / (2 * np.sqrt(2) * sigma))
    return A * ((f1 - f2) / f3) + bg

# Left and right Gaussians
#left_gaussian = A * np.exp(-((x - (x0 - w/2))**2) / (2 * sigma**2))
#right_gaussian = A * np.exp(-((x - (x0 + w/2))**2) / (2 * sigma**2))

# Plot
plt.figure(figsize=(9,5))

plt.plot(xs, flat_top(xs, 1, 1, 15, 5, 2), 'k', lw=3, label='Flat-top Gaussian')
#plt.plot(x, left_gaussian, '--b', lw=2, label='Left Gaussian')
#plt.plot(x, right_gaussian, '--r', lw=2, label='Right Gaussian')

# Plateau edges
#plt.axvline(x0 - w/2, color='gray', ls=':', alpha=0.7)
#plt.axvline(x0 + w/2, color='gray', ls=':', alpha=0.7)

plt.xlabel('x')
plt.ylabel('Amplitude')
plt.title('Flat-top Gaussian and the Two Underlying Gaussian Wings')
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()