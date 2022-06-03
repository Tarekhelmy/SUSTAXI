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

    # Upper Sheet - curved approx.
    Upper_sheet = [[x_te] + Airfoil_upper[0][idx_te_up:idx_le_up] + [x_le],
                   [y_te_up] + Airfoil_upper[1][idx_te_up:idx_le_up] + [y_le_up]]
    Lower_sheet = [[x_le] + Airfoil_lower[0][idx_le_low:idx_te_low] + [x_te],
                   [y_le_low] + Airfoil_lower[1][idx_le_low:idx_te_low] + [y_te_low]]

    """plt.plot(Airfoil_shape[0], Airfoil_shape[1], ls='--')
    plt.plot(Upper_sheet[0] + Lower_sheet[0] + [Upper_sheet[0][0]], Upper_sheet[1] + Lower_sheet[1] + [Upper_sheet[1][0]])

    plt.xlim(0,1)
    plt.ylim(-0.5,0.5)
    plt.grid()
    plt.show()"""


    # ======== I_yy of Wingbox without stringers --> Times c^3 ==========
    y_centroid = np.average(Upper_sheet[1] + Lower_sheet[1])
    #print('y_centroid=', y_centroid)
    #plt.scatter(0.5, y_centroid)
    I_yy_sheet_upper_lst = []
    t_upper = 0.003  # m
    for i in range(len(Upper_sheet[0])):
        x_1 = Upper_sheet[0][i-1]
        x_2 = Upper_sheet[0][i]
        y_1 = Upper_sheet[1][i-1]
        y_2 = Upper_sheet[1][i]
        b = ((x_1-x_2)**2+(y_2-y_1)**2)**0.5
        I_yy_sheet_element = b * t_upper * ((y_1+y_2)/2-y_centroid)**2
        I_yy_sheet_upper_lst.append(I_yy_sheet_element)
    I_yy_sheet_upper = sum(I_yy_sheet_upper_lst)

    I_yy_sheet_lower_lst = []
    t_lower = 0.003  # m
    for i in range(len(Lower_sheet[0])):
        x_1 = Lower_sheet[0][i-1]
        x_2 = Lower_sheet[0][i]
        y_1 = Lower_sheet[1][i-1]
        y_2 = Lower_sheet[1][i]
        b = ((x_1-x_2)**2+(y_2-y_1)**2)**0.5
        I_yy_sheet_element = b * t_lower * ((y_1+y_2)/2-y_centroid)**2
        I_yy_sheet_lower_lst.append(I_yy_sheet_element)
    I_yy_sheet_lower = sum(I_yy_sheet_lower_lst)

    t_le = 0.008    # m
    t_te = 0.008    # m
    I_yy_LE = (y_le_up-y_le_low)**3 * t_le/12 + (y_le_up-y_le_low) * t_le * ((y_le_up-y_le_low)/2-y_centroid)**2
    I_yy_TE = (y_te_up-y_te_low)**3 * t_te/12 + (y_te_up-y_te_low) * t_te * ((y_te_up-y_te_low)/2-y_centroid)**2
    #print(I_yy_TE+I_yy_LE+I_yy_sheet_upper+I_yy_sheet_lower)
    I_yy_box = I_yy_TE+I_yy_LE+I_yy_sheet_upper+I_yy_sheet_lower

    return I_yy_box, Upper_sheet, Lower_sheet
    #return x_le, x_te, y_le_up, y_te_up, y_le_low, y_te_low, Ixx_t, points, x_cent, y_cent, Upper_sheet, Lower_sheet
#x_le, x_te, y_le_up, y_te_up, y_le_low, y_te_low, Ixx_t, points, x_cent, y_cent = wing_box(0.15, 0.7)
#wing_box(0.15, 0.7)
#wing_box(0.1, 0.65)
#wing_box(0.2, 0.75)

I_yy_box, Upper_sheet, Lower_sheet = wing_box(0.15, 0.7)
'''print(Ixx_t)
plt.plot(Airfoil_shape[0], Airfoil_shape[1])
plt.scatter(x_mid(), y_mid(), marker='+')
plt.plot([x_le, x_le, x_te, x_te, x_le], [y_le_up, y_le_low, y_te_low, y_te_up, y_le_up], ls='--')
plt.scatter(x_cent, y_cent, marker='x')
plt.xlim(0, 1)
plt.ylim(-0.5, 0.5)
plt.grid()
plt.show()'''

box_centre = np.average(Upper_sheet[1] + Lower_sheet[1])
y_dist = max(Airfoil_shape[1])-box_centre
#print('maximum y distance =', y_dist, 'of chord')
'''
# Stringers (L-shape)
L_base = 100 # mm
L_web = 100 # mm
t_str_L = 3 # mm
A_str_L = L_base*t_str_L + L_web*t_str_L
cent_y_str_L = (L_base * t_str_L * t_str_L/2 + L_web * t_str_L * L_web/2)/(L_base * t_str_L + L_web * t_str_L)
I_yy_str_L = t_str_L*L_web**3/12 + (L_web/2 - cent_y_str_L)**2 * L_web*t_str_L \
           + (cent_y_str_L - t_str_L/2)**2 * L_base*t_str_L


# Z-shape
Z_base = 50     # mm
Z_web = 100     # mm
Z_top = 50      # mm
t_str_Z = 3       # mm
A_str_Z = Z_base*t_str_Z + Z_web*t_str_Z + Z_top*t_str_Z
cent_y_str_Z = Z_web/2
I_yy_str_Z = t_str_Z*Z_web**3/12 \
            + (cent_y_str_Z - t_str_Z/2)**2 * (Z_base + Z_top) *t_str_Z

# Add Stringers
I_yy_four_corner_str = 4*I_yy_str_L \
                      + A_str_L*((Upper_sheet[1][0]-box_centre)**2 + (Upper_sheet[1][-1]-box_centre)**2 +
                                 (Lower_sheet[1][0]-box_centre)**2 + (Lower_sheet[1][-1]-box_centre)**2)

#print(I_yy_four_corner_str)
'''