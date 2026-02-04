import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.optimize import curve_fit

FILENAME = "C:\\Users\\au601136\\OneDrive - Aarhus universitet\\Skrivebord\\AFM data\\20260114\\y16_section3.txt"

VERT_CAL = 1.026
LAT_CAL = 1.031
BOW_NM_100UM = 19.5

TIP_THETA_LEFT_DEG = 15.0
TIP_THETA_RIGHT_DEG = 25.0
R_TIP_NM = 10.0 #tip radius

X_MIN_NM = 0
X_MAX_NM = 700

def slope_correction(xs: np.ndarray, ys: np.ndarray) -> np.ndarray: ## fix the slope_correction function!!!!
    def lin_fit(x, a, b, c):
        return a**(x*b) + c

    popt, pcov = curve_fit(lin_fit, xs, ys)
    ys = [y-lin_fit(x, *popt) for x,y in zip(xs, ys)]
    return np.array(ys)

def tip_profile_asymmetric(d_nm: np.ndarray, thetaL_deg: float, thetaR_deg: float, R_tip_nm: float) -> np.ndarray:
    d = np.asarray(d_nm, dtype=float)
    thL = np.deg2rad(thetaL_deg)
    thR = np.deg2rad(thetaR_deg)

    wedge = np.where(d >= 0.0, d / np.tan(thR), (-d) / np.tan(thL))
    R = float(R_tip_nm)
    sphere = np.full_like(d, np.inf, dtype=float)
    mask = np.abs(d) < R
    sphere[mask] = R - np.sqrt(np.maximum(R**2 - d[mask]**2, 0.0))    
    return np.minimum(wedge, sphere)


def apply_tip_max_convolution(x_nm: np.ndarray, z_true_nm: np.ndarray, thetaL_deg: float, thetaR_deg: float, R_tip_nm: float, max_range_nm: float = 800.0) -> np.ndarray:
    x = np.asarray(x_nm, dtype=float)
    zt = np.asarray(z_true_nm, dtype=float)
    N = len(x)
    zm = np.empty(N, dtype=float)
    for i in range(N):
        lo = np.searchsorted(x, x[i] - max_range_nm, side="left")
        hi = np.searchsorted(x, x[i] + max_range_nm, side="right")
        d = x[i] - x[lo:hi]
        tip = tip_profile_asymmetric(d, thetaL_deg, thetaR_deg, R_tip_nm)
        zm[i] = np.max(zt[lo:hi] - tip)
    return zm       


def two_top_trapezoid_true_theta(x_nm: np.ndarray, H: float, P: float, w1: float, w2: float, theta_wall_deg: float, g1: float, X0: float, Z0: float, Tilt: float) -> np.ndarray:
    x = np.asarray(x_nm, dtype=float)

    if H <= 0 or P <= 0 or w1 <= 0 or w2 <= 0 or g1 <= 0:
        return 1e9 * np.ones_like(x)
    theta = np.deg2rad(theta_wall_deg)
    o = H * np.tan(theta)           
    g2 = P - (w1 + w2 + 4.0 * o + g1)
    if o <= 0 or g2 <= 0:
        return 1e9 * np.ones_like(x)

    Px = np.array([0.0, 
                   o, 
                   o + w1, 2*o + w1, 
                   2*o + w1 + g1, 
                   3*o + w1 + g1, 3*o + w1 + g1 + w2, 
                   4*o + w1 + g1 + w2, 
                   P])

    Pz = np.array([0.0, H, H, 0.0, 0.0, H, H, 0.0, 0.0])

    x_mod = np.mod(x - X0, P)
    z_mod = np.interp(x_mod, Px, Pz)
    return z_mod + Z0 + Tilt * x

def model_measured(p: np.ndarray, x_nm: np.ndarray) -> np.ndarray:
    H, P, w1, w2, theta_wall_deg, g1, X0, Z0, Tilt = p
    z_true = two_top_trapezoid_true_theta(x_nm, H, P, w1, w2, theta_wall_deg, g1, X0, Z0, Tilt)

    if np.any(z_true > 1e8):
        return z_true
    z_meas = apply_tip_max_convolution(x_nm, z_true, thetaL_deg=TIP_THETA_LEFT_DEG, thetaR_deg=TIP_THETA_RIGHT_DEG, R_tip_nm=R_TIP_NM, max_range_nm=800.0)
    return z_meas

def residuals(p: np.ndarray, x_nm: np.ndarray, z_nm: np.ndarray) -> np.ndarray:
    return model_measured(p, x_nm) - z_nm   


data = np.genfromtxt(FILENAME, encoding="latin-1", skip_header=1)
data = data[~np.isnan(data).any(axis=1)]

x = data[:, 0].astype(float)
z = data[:, 1].astype(float)

x_nm = x * 1000.0

z_nm = z

z_nm = np.array([z-np.min(z_nm) for z in z_nm])


x_nm = x_nm / LAT_CAL
z_nm = z_nm / VERT_CAL
z_nm = z_nm + BOW_NM_100UM * (x_nm / 50e3) ** 2


if X_MIN_NM is not None:
    m = x_nm >= X_MIN_NM
    x_nm, z_nm = x_nm[m], z_nm[m]
if X_MAX_NM is not None:
    m = x_nm <= X_MAX_NM
    x_nm, z_nm = x_nm[m], z_nm[m]
# Ensure sorted by x
idx = np.argsort(x_nm)
x_nm = x_nm[idx]
z_nm = z_nm[idx]


# p = [H, P, w1, w2, theta_wall_deg, g1, X0, Z0, Tilt]
p0 = np.array([
    125.0, # H (nm)
    510.0, # P (nm)
    80.0, # w1 (nm)
    50.0, # w2 (nm)
    25.0, # theta_wall_deg (from vertical)
    7.0, # g1 (nm)
    0.0, # X0 (nm)
    0.0, # Z0 (nm)
    0.0 # Tilt (nm/nm)
    ], dtype=float)

lb = np.array([
    10.0, # H
    450.0, # P
    20.0, # w1
    20.0, # w2
    0.5, # theta_wall_deg
    1.0, # g1
    -2000.0, # X0
    -1e4, # Z0
    -0.05 # Tilt
    ], dtype=float)

ub = np.array([
    500.0, # H
    650.0, # P
    400.0, # w1
    400.0, # w2
    80.0, # theta_wall_deg
    800.0, # g1
    2000.0, # X0
    1e4, # Z0
    0.05 # Tilt
    ], dtype=float)

res = least_squares(
    residuals,
    p0,
    bounds=(lb, ub),
    args=(x_nm, z_nm),
    max_nfev=10000
    )

p_fit = res.x
H, P_fit, w1_fit, w2_fit, theta_wall_deg, g1_fit, X0_fit, Z0_fit, Tilt_fit = p_fit


o_fit = H * np.tan(np.deg2rad(theta_wall_deg))
g2_fit = P_fit - (w1_fit + w2_fit + 4.0 * o_fit + g1_fit)

z_fit = model_measured(p_fit, x_nm)

print("\n=== Fit results (sample geometry + tip forward model) ===")
print(f"Tip model: thetaL={TIP_THETA_LEFT_DEG}°, thetaR={TIP_THETA_RIGHT_DEG}°, R={R_TIP_NM} nm")
print(f"H = {H:.3f} nm")
print(f"P = {P_fit:.3f} nm")
print(f"w1 = {w1_fit:.3f} nm")
print(f"w2 = {w2_fit:.3f} nm")
print(f"theta_wall (sample, shared) = {theta_wall_deg:.3f} deg (from vertical)")
print(f"offset (derived run per wall) = {o_fit:.3f} nm")
print(f"g1 = {g1_fit:.3f} nm")
print(f"g2 = {g2_fit:.3f} nm (derived closing gap; should be > 0)")
print(f"X0 = {X0_fit:.3f} nm")
print(f"Z0 = {Z0_fit:.3f} nm")
print(f"Tilt = {Tilt_fit:.6g} nm/nm")
print(f"Cost = {res.cost:.6g} (0.5*sum(residual^2))")
print(f"Status = {res.status} ({res.message})")

plt.figure(figsize=(10, 6))
plt.plot(x_nm, z_nm, ".", ms=4, label="AFM data (calibrated + bow)")
plt.plot(x_nm, z_fit, "-", lw=2, label="Fit (dual-top + asymmetric tip + radius)")
plt.xlabel("x (nm)")
plt.ylabel("z (nm)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

