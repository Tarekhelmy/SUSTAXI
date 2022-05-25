import matplotlib.pyplot as plt
import numpy as np
# NACA 63-412
Airfoil_shape = [[1.000000, 0.950230, 0.900490, 0.850700, 0.800840, 0.750890, 0.700870, 0.650760, 0.600570, 0.550310, 0.500000, 0.449640, 0.399240, 0.348820, 0.298400, 0.248000, 0.197650, 0.147350, 0.097180, 0.072180, 0.047270, 0.022570, 0.010410, 0.005670, 0.003360, 0.000000, 0.006640, 0.009330, 0.014590, 0.027430, 0.052730, 0.077820, 0.102820, 0.152650, 0.202350, 0.252000, 0.301600, 0.351118, 0.400760, 0.450350, 0.500000, 0.549690, 0.599430, 0.649240, 0.699130, 0.749110, 0.799160, 0.849300, 0.899510, 0.949770, 1.000000],
                  [ 0.000000, 0.008810, 0.017390, 0.026180, 0.034920, 0.043440, 0.051530, 0.058990, 0.065620, 0.071250, 0.075670, 0.078940, 0.080620, 0.080590, 0.078720, 0.074990, 0.069290, 0.061380, 0.050630, 0.043790, 0.035440, 0.024600, 0.017190, 0.013200, 0.010710, 0.000000, -0.008710, -0.010400, -0.012910, -0.017160, -0.022800, -0.026850, -0.029950, -0.034460, -0.037450, -0.039190, -0.039840, -0.039390, -0.037780, -0.035140, -0.031640, -0.027450, -0.022780, -0.017990, -0.012650, -0.007640, -0.003080, 0.000740, 0.003290, 0.003300, 0.000000]]
Airfoil_upper = [Airfoil_shape[0][0:Airfoil_shape[0].index(0)], Airfoil_shape[1][0:Airfoil_shape[0].index(0)]]
Airfoil_lower = [Airfoil_shape[0][Airfoil_shape[0].index(0):], Airfoil_shape[1][Airfoil_shape[0].index(0):]]
print(Airfoil_upper)
print(Airfoil_lower)


# Wing planform
AR = 10
S = 30.34   # m^2
b = np.sqrt(S*AR)
taper = 0.4
c_root = S/b*2 / (1+taper)
c_tip = c_root*taper
print(c_root, c_tip)

# Elliptical lift distribution
y_wing = np.arange(0,101,1)
a = 1
b = 1
Lift_distribution_y = np.sqrt((y_wing**2 / 1 + 1) * b)

# I_xx = b * h^3 / 12 + A*d^2
# <<<< for horizontal elements: >>>>
# I_xx = (b) * t^3 * cos^2(beta) / 12 + (b) * t * (d)^2
# d = (x_left + x_right) / 2 - x_centroid
# <<<< for vertical elements: >>>>
# I_xx = t * (h)^3 * sin^2(beta) / 12 + t * (h) * (d)^2
# d = (y_upper + y_lower) / 2 - y_centroid

x_avg = np.average(Airfoil_shape[0])
y_avg = np.average(Airfoil_shape[1])
print(x_avg)
print(y_avg)

def x_mid():
    A_x_list = []
    A_list = []
    for i in range(len(Airfoil_shape[0])):
        A_i = abs((Airfoil_shape[0][i]-Airfoil_shape[0][i-1])\
              * (Airfoil_shape[1][i]+Airfoil_shape[1][i-1])/2)   # Incremental area
        x_Area = (Airfoil_shape[0][i]+Airfoil_shape[0][i-1])/2  # Average x of increment
        A_x = A_i * x_Area  # Area moment
        A_list.append(A_i)
        A_x_list.append(A_x)
    A_x_sum = sum(A_x_list)
    A_sum = sum(A_list)
    x_c = A_x_sum/A_sum
    return x_c
print(x_mid())

def y_mid():
    A_y_list = []
    A_list = []
    for i in range(len(Airfoil_shape[0])):
        A_i = abs((Airfoil_shape[0][i]-Airfoil_shape[0][i-1])\
              * (Airfoil_shape[1][i]+Airfoil_shape[1][i-1])/2)   # Incremental area
        y_Area = (Airfoil_shape[1][i]+Airfoil_shape[1][i-1])/2  # Average y of increment
        A_y = A_i * y_Area  # Area moment
        A_list.append(A_i)
        A_y_list.append(A_y)
    A_y_sum = sum(A_y_list)
    A_sum = sum(A_list)
    y_c = A_y_sum/A_sum
    return y_c
print(y_mid())


# Second Area Moment
# Thin wall assumption used --> t^3 terms are omitted, the I_xx_... terms are ...* t

def I_xx_upper(x_1, x_2):
    idx_1 = Airfoil_shape[0].index(x_1)
    idx_2 = Airfoil_shape[0].index(x_2)
    y_1 = Airfoil_shape[1][idx_1]
    y_2 = Airfoil_shape[1][idx_2]
    b_up = np.sqrt((x_2-x_1)**2 + (y_2-y_1)**2)
    beta_up = abs(np.arcsin(abs(y_2-y_1)/b_up))
    d_up = (y_1 + y_2)/2 - y_mid()
    # I_xx_u = (b_u) * t ^ 3 * np.cos(beta)**2 / 12 + (b) * t * (d_u) ^ 2  >>>>  assuming small thickness
    I_xx_up =  b_up * d_up**2   # ...* t
    return I_xx_up


def I_xx_lower(x_3, x_4):
    idx_3 = Airfoil_shape[0].index(x_3)
    idx_4 = Airfoil_shape[0].index(x_4)
    y_3 = Airfoil_shape[1][idx_3]
    y_4 = Airfoil_shape[1][idx_4]
    b_low = np.sqrt((x_4 - x_3) ** 2 + (y_4 - y_3) ** 2)
    beta_low = abs(np.arcsin(abs(y_4 - y_3) / b_low))
    d_low = (y_3 + y_4) / 2 - y_mid()
    # I_xx_l = (b_u) * t ^ 3 * np.cos(beta)**2 / 12 + (b) * t * (d_u) ^ 2  >>>>  assuming small thickness
    I_xx_low = b_low * d_low ** 2  # ...* t
    return I_xx_low


def I_xx_lead(x_2, x_3):
    idx_2 = Airfoil_shape[0].index(x_2)
    idx_3 = Airfoil_shape[0].index(x_3)
    y_2 = Airfoil_shape[1][idx_2]
    y_3 = Airfoil_shape[1][idx_3]
    h_le = np.sqrt((x_3 - x_2) ** 2 + (y_3 - y_2) ** 2)
    beta_le = abs(np.arcsin(abs(y_3 - y_2) / h_le))
    d_le = (y_3 + y_2)/2 - y_mid()
    # I_xx = t * (h)^3 * sin^2(beta) / 12 + t *1(h) * (d)^2
    I_xx_le = h_le**3 * np.sin(beta_le)**2 / 12 + h_le * d_le**2    # ...* t
    return I_xx_le


def I_xx_trail(x_1, x_4):
    idx_1 = Airfoil_shape[0].index(x_1)
    idx_4 = Airfoil_shape[0].index(x_4)
    y_1 = Airfoil_shape[1][idx_1]
    y_4 = Airfoil_shape[1][idx_4]
    h_te = np.sqrt((x_4 - x_1)**2 + (y_4 - y_1)**2)
    beta_te = abs(np.arcsin(abs(y_4-y_1)/h_te))
    d_te = (y_4 + y_1)/2 - y_mid()
    # I_xx = t * (h)^3 * sin^2(beta) / 12 + t * (h) * (d)^2
    I_xx_te = h_te**3 * np.sin(beta_te)**2 / 12 + h_te * d_te**2    # ...* t
    return I_xx_te

# Optimization Algorithm
I_xx_list = []
x_list = []
for i in range(len(Airfoil_upper[0])):
    x_1 = Airfoil_upper[0][i]
    if x_1 <= 0.75 and x_1 >= 0.2:
        for j in range(len(Airfoil_upper[0])):
            x_2 = Airfoil_upper[0][j]
            if x_2 <= 0.75 and x_2 >= 0.2:
                for k in range(len(Airfoil_lower[0])):
                    x_3 = Airfoil_lower[0][k]
                    if x_3 <= 0.75 and x_3 >= 0.2:
                        for n in range(len(Airfoil_lower[0])):
                            x_4 = Airfoil_lower[0][n]
                            if x_4 <= 0.75 and x_4 >= 0.2:
                                I_xx_tot = I_xx_upper(x_1, x_2) + I_xx_lower(x_3, x_4) + I_xx_lead(x_1, x_3) + I_xx_trail(
                                    x_2, x_4)
                                I_xx_list.append(I_xx_tot)
                                x_list.append([x_1, x_2, x_3, x_4])
                            else:
                                pass
                    else:
                        pass
            else:
                pass
    else:
        pass
    print(i)


print(I_xx_list)
print(len(x_list))
max_I_xx = max(I_xx_list)
print(x_list[I_xx_list.index(max_I_xx)])
x_1, x_2, x_3, x_4 = x_list[I_xx_list.index(max_I_xx)]
points_box = [x_list[I_xx_list.index(max_I_xx)], [Airfoil_shape[1][Airfoil_shape[0].index(x_1)], Airfoil_shape[1][Airfoil_shape[0].index(x_2)],
                                                        Airfoil_shape[1][Airfoil_shape[0].index(x_3)], Airfoil_shape[1][Airfoil_shape[0].index(x_4)]]]
print(I_xx_list[I_xx_list.index(max_I_xx)])
print(I_xx_list[77], x_list[77])
plt.plot(Airfoil_shape[0], Airfoil_shape[1])
plt.scatter(x_mid(), y_mid(), marker='+')
plt.xlim(0, 1)
plt.ylim(-0.5, 0.5)
plt.scatter(points_box[0][0], points_box[1][0])
plt.scatter(points_box[0][1], points_box[1][1])
plt.scatter(points_box[0][2], points_box[1][2])
plt.scatter(points_box[0][3], points_box[1][3])
plt.grid()
plt.show()

plt.plot(I_xx_list)
plt.show()