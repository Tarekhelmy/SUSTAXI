import numpy as np
import matplotlib.pyplot as plt
#from Wing_box_optimisation import I_xx_trail, I_xx_lead, I_xx_upper, I_xx_lower

# Airfoil from Airfoiltools (NACA 63 412)
Airfoil_shape = [[1.000000, 0.950230, 0.900490, 0.850700, 0.800840, 0.750890, 0.700870, 0.650760, 0.600570, 0.550310, 0.500000, 0.449640, 0.399240, 0.348820, 0.298400, 0.248000, 0.197650, 0.147350, 0.097180, 0.072180, 0.047270, 0.022570, 0.010410, 0.005670, 0.003360, 0.000000, 0.006640, 0.009330, 0.014590, 0.027430, 0.052730, 0.077820, 0.102820, 0.152650, 0.202350, 0.252000, 0.301600, 0.351118, 0.400760, 0.450350, 0.500000, 0.549690, 0.599430, 0.649240, 0.699130, 0.749110, 0.799160, 0.849300, 0.899510, 0.949770, 1.000000],
                 [0.000000, 0.008810, 0.017390, 0.026180, 0.034920, 0.043440, 0.051530, 0.058990, 0.065620, 0.071250, 0.075670, 0.078940, 0.080620, 0.080590, 0.078720, 0.074990, 0.069290, 0.061380, 0.050630, 0.043790, 0.035440, 0.024600, 0.017190, 0.013200, 0.010710, 0.000000, -0.008710, -0.010400, -0.012910, -0.017160, -0.022800, -0.026850, -0.029950, -0.034460, -0.037450, -0.039190, -0.039840, -0.039390, -0.037780, -0.035140, -0.031640, -0.027450, -0.022780, -0.017990, -0.012650, -0.007640, -0.003080, 0.000740, 0.003290, 0.003300, 0.000000]]
Airfoil_upper = [Airfoil_shape[0][0:Airfoil_shape[0].index(0)], Airfoil_shape[1][0:Airfoil_shape[0].index(0)]]
Airfoil_lower = [Airfoil_shape[0][Airfoil_shape[0].index(0):], Airfoil_shape[1][Airfoil_shape[0].index(0):]]


# Centroid
def x_mid():
    A_x_list = []
    A_list = []
    for i in range(len(Airfoil_shape[0])):
        A_i = (Airfoil_shape[0][i]-Airfoil_shape[0][i-1])\
              * (Airfoil_shape[1][i]+Airfoil_shape[1][i-1])/2   # Incremental area
        x_Area = (Airfoil_shape[0][i]+Airfoil_shape[0][i-1])/2  # Average x of increment
        A_x = A_i * x_Area  # Area moment
        A_list.append(A_i)
        A_x_list.append(A_x)
    A_x_sum = sum(A_x_list)
    A_sum = sum(A_list)
    x_c = A_x_sum/A_sum
    return x_c

def y_mid():
    A_y_list = []
    A_list = []
    for i in range(len(Airfoil_shape[0])):
        A_i = (Airfoil_shape[0][i]-Airfoil_shape[0][i-1])\
              * (Airfoil_shape[1][i]+Airfoil_shape[1][i-1])/2   # Incremental area
        y_Area = (Airfoil_shape[1][i]+Airfoil_shape[1][i-1])/2  # Average y of increment
        A_y = A_i * y_Area  # Area moment
        A_list.append(A_i)
        A_y_list.append(A_y)
    A_y_sum = sum(A_y_list)
    A_sum = sum(A_list)
    y_c = A_y_sum/A_sum
    return y_c

def wing_box(x_le, x_te):
    upper_array = np.asarray(Airfoil_upper)
    lower_array = np.asarray(Airfoil_lower)
    # Leading Edge
    idx_le_up = (np.abs(upper_array[0] - x_le)).argmin()
    idx_le_low = (np.abs(lower_array[0] - x_le)).argmin()
    # Upper
    if upper_array[0][idx_le_up] - x_le >= 0:
        x_1 = upper_array[0][idx_le_up]
        x_2 = upper_array[0][idx_le_up+1]
        y_1 = upper_array[1][idx_le_up]
        y_2 = upper_array[1][idx_le_up+1]
        y_le_up = y_1 + (y_2-y_1)/(x_2-x_1)*(x_le-x_1)
    if upper_array[0][idx_le_up] - x_le < 0:
        x_1 = upper_array[0][idx_le_up-1]
        x_2 = upper_array[0][idx_le_up]
        y_1 = upper_array[1][idx_le_up-1]
        y_2 = upper_array[1][idx_le_up]
        y_le_up = y_1 + (y_2 - y_1) / (x_2 - x_1) * (x_le - x_1)
    # Lower
    if lower_array[0][idx_le_low] - x_le >= 0:
        x_1 = lower_array[0][idx_le_low]
        x_2 = lower_array[0][idx_le_low + 1]
        y_1 = lower_array[1][idx_le_low]
        y_2 = lower_array[1][idx_le_low + 1]
        y_le_low = y_1 + (y_2 - y_1) / (x_2 - x_1) * (x_le - x_1)
    if lower_array[0][idx_le_low] - x_le < 0:
        x_1 = lower_array[0][idx_le_low-1]
        x_2 = lower_array[0][idx_le_low]
        y_1 = lower_array[1][idx_le_low-1]
        y_2 = lower_array[1][idx_le_low]
        y_le_low = y_1 + (y_2 - y_1) / (x_2 - x_1) * (x_le - x_1)

    # Trailing Edge
    idx_te_up = (np.abs(upper_array[0] - x_te)).argmin()
    idx_te_low = (np.abs(lower_array[0] - x_te)).argmin()
    # Upper
    if upper_array[0][idx_te_up] - x_te >= 0:
        x_1 = upper_array[0][idx_te_up]
        x_2 = upper_array[0][idx_te_up+1]
        y_1 = upper_array[1][idx_te_up]
        y_2 = upper_array[1][idx_te_up+1]
        y_te_up = y_1 + (y_2-y_1)/(x_2-x_1)*(x_te-x_1)
    if upper_array[0][idx_te_up] - x_te < 0:
        x_1 = upper_array[0][idx_te_up-1]
        x_2 = upper_array[0][idx_te_up]
        y_1 = upper_array[1][idx_te_up-1]
        y_2 = upper_array[1][idx_te_up]
        y_te_up = y_1 + (y_2 - y_1) / (x_2 - x_1) * (x_te - x_1)
    # Lower
    if lower_array[0][idx_te_low] - x_te >= 0:
        x_1 = lower_array[0][idx_te_low]
        x_2 = lower_array[0][idx_te_low + 1]
        y_1 = lower_array[1][idx_te_low]
        y_2 = lower_array[1][idx_te_low + 1]
        y_te_low = y_1 + (y_2 - y_1) / (x_2 - x_1) * (x_te - x_1)
    if lower_array[0][idx_te_low] - x_te < 0:
        x_1 = lower_array[0][idx_te_low-1]
        x_2 = lower_array[0][idx_te_low]
        y_1 = lower_array[1][idx_te_low-1]
        y_2 = lower_array[1][idx_te_low]
        y_te_low = y_1 + (y_2 - y_1) / (x_2 - x_1) * (x_te - x_1)

    # Centroid
    x_cent = (x_le + x_te)/2
    y_cent = (y_le_up + y_te_up + y_le_low + y_te_low)/4

    # Bending Resistance (Ixx(t))
    # Upper Sheet
    b_up = np.sqrt((x_te - x_le) ** 2 + (y_le_up - y_te_up) ** 2)
    beta_up = abs(np.arcsin(abs(y_le_up - y_te_up) / b_up))
    d_up = (y_le_up + y_te_up) / 2 - y_cent
    # I_xx_u = (b_u) * t ^ 3 * np.cos(beta)**2 / 12 + (b) * t * (d_u) ^ 2  >>>>  assuming small thickness
    I_xx_up = b_up * d_up ** 2  # ...* t

    # Lower Sheet
    b_low = np.sqrt((x_te - x_le) ** 2 + (y_te_low - y_le_low) ** 2)
    beta_low = abs(np.arcsin(abs(y_te_low - y_le_low) / b_low))
    d_low = (y_le_low + y_te_low) / 2 - y_cent
    # I_xx_l = (b_u) * t ^ 3 * np.cos(beta)**2 / 12 + (b) * t * (d_u) ^ 2  >>>>  assuming small thickness
    I_xx_low = b_low * d_low ** 2  # ...* t

    # Leading Sheet
    h_le = np.sqrt((y_le_up - y_le_low))
    d_le = (y_le_up + y_le_low) / 2 - y_cent
    # I_xx = t * (h)^3 * sin^2(beta) / 12 + t *1(h) * (d)^2
    I_xx_le = h_le ** 3 / 12 + h_le * d_le ** 2  # ...* t

    # Trailing Sheet
    h_te = np.sqrt((y_te_up - y_te_low))
    d_te = (y_te_up + y_te_low) / 2 - y_cent
    # I_xx = t * (h)^3 * sin^2(beta) / 12 + t *1(h) * (d)^2
    I_xx_te = h_te ** 3 / 12 + h_te * d_te ** 2  # ...* t

    Ixx_t = I_xx_up + I_xx_low + I_xx_le + I_xx_te
    points = [[y_le_up, x_le], [y_le_low, x_le], [y_te_low, x_te], [y_te_low, x_te]]

    return x_le, x_te, y_le_up, y_te_up, y_le_low, y_te_low, Ixx_t, points, x_cent, y_cent
x_le, x_te, y_le_up, y_te_up, y_le_low, y_te_low, Ixx_t, points, x_cent, y_cent = wing_box(0.15, 0.7)
#print(wing_box(0.2, 0.75))
print(Ixx_t)
plt.plot(Airfoil_shape[0], Airfoil_shape[1])
plt.scatter(x_mid(), y_mid(), marker='+')
plt.plot([x_le, x_le, x_te, x_te, x_le], [y_le_up, y_le_low, y_te_low, y_te_up, y_le_up], ls='--')
plt.scatter(x_cent, y_cent, marker='x')
plt.xlim(0, 1)
plt.ylim(-0.5, 0.5)
plt.grid()
plt.show()

y_dist = max(Airfoil_shape[1])-y_mid()
print('maximum y distance =', y_dist, 'of chord')

