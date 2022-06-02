from Aero_Tools.Wing_box_adsee import y_dist, wing_box
from Wing_Calculator import lift, comp_halfdata, trailingedgeangle, leadingedgeangle, c_r, engine
import numpy as np
import math as mt
import matplotlib.pyplot as plt



n_safety=1.5
n_load = 4.6

# ======= Materials =======
# Aluminium 7075
E_al7050 = 71.7 # GPa
UTS_al7050 = 572 # MPa
YTS_al7050 = 469 # MPa
poisson_al7050 = 0.33
G_al7050 = 26.9 # GPa

# Aluminium 7050
E_al7050 = 75 # GPa --> The sources say 70 - 80 GPa ...
UTS_al7050 = 515 # MPa
YTS_al7050 = 455 # MPa
poisson_al7050 = 0.33
G_al7050 = 26.9 # GPa

def Mz():
    Mz = (abs(comp_halfdata[1:,0])+ abs(comp_halfdata[:-1,0]))/2 * (((lift()+engine())*n_load))
    Mn = ()
    for i in range(0,len(Mz)+1,1):
        Mn += (sum(Mz[:i]),)
    return Mn




#plt.plot(comp_halfdata[:,0],Mz())
#plt.show()

"calculating chord at x coordinates"
def chord():
    z_coords = (abs(comp_halfdata[1:,0])+ abs(comp_halfdata[:-1,0]))/2
    return c_r() - z_coords*mt.tan(trailingedgeangle()) - z_coords*mt.tan(leadingedgeangle())


"Bending required I_yy at each point along span"
yy = chord()*y_dist
mz = np.array(Mz())
sigma = YTS_al7050/n_safety*10**6
i_yy = (mz[1:]*yy)/sigma
"scaled calculates I_yy of the sheet at every x position"
scaled = wing_box(0.15, 0.7)[0] * ((chord())**3)

"req_I_yy is the remaining I_yy that has to be satisfied with stringers"
req_I_yy = i_yy - scaled

"buckling"

def buckling():
    C = 4
    b = 0.55
    t = 4 #mm
    return (C*np.pi*np.pi*E_al7050/(12*(1-poisson_al7050)))*((t/b)**2)



I_yy_box, Upper_sheet, Lower_sheet = wing_box(0.15, 0.7)

box_centre = np.average(Upper_sheet[1] + Lower_sheet[1])

# Stringers (L-shape)
L_base = 30 # mm
L_web = 30 # mm
t_str_L = 5 # mm
A_str_L = L_base*t_str_L + L_web*t_str_L
cent_y_str_L = (L_base * t_str_L * t_str_L/2 + L_web * t_str_L * L_web/2)/(L_base * t_str_L + L_web * t_str_L)
I_yy_str_L = t_str_L*L_web**3/12 + (L_web/2 - cent_y_str_L)**2 * L_web*t_str_L \
             + (cent_y_str_L - t_str_L/2)**2 * L_base*t_str_L


# Z-shape
Z_base = 20     # mm
Z_web = 50     # mm
Z_top = 20      # mm
t_str_Z = 5       # mm
A_str_Z = Z_base*t_str_Z + Z_web*t_str_Z + Z_top*t_str_Z
cent_y_str_Z = Z_web/2
I_yy_str_Z = t_str_Z*Z_web**3/12 \
             + (cent_y_str_Z - t_str_Z/2)**2 * (Z_base + Z_top) *t_str_Z

# Add Stringers
I_yy_four_corner_str = 4*I_yy_str_L * 10**-12 \
                       + A_str_L*10**-6*((Upper_sheet[1][0]-box_centre)**2 + (Upper_sheet[1][-1]-box_centre)**2 +
                                  (Lower_sheet[1][0]-box_centre)**2 + (Lower_sheet[1][-1]-box_centre)**2) * (chord())**2

print(req_I_yy - I_yy_four_corner_str)
req_I_yy = req_I_yy - I_yy_four_corner_str

# Average height
y_top_avg = np.average(Upper_sheet[1])       # * chord
y_bottom_avg = np.average(Lower_sheet[1])    # * chord
print('y_bot=', y_bottom_avg)

dist_top_avg = abs((y_top_avg - box_centre) * chord()) - Z_web/1000/2
dist_bottom_avg = abs((y_bottom_avg - box_centre) * chord()) - Z_web/1000/2

I_yy_top_str = I_yy_str_Z *10**-12 + dist_top_avg**2 * A_str_Z *10**-6
I_yy_bottom_str = I_yy_str_Z *10**-12 + dist_bottom_avg**2 * A_str_Z *10**-6

n_str_pos = []
for i in range(len(req_I_yy)):
    if req_I_yy[i] > 0:
        n_str_req = mt.ceil(req_I_yy[i]/(I_yy_top_str[i]+I_yy_bottom_str[i]))
    else:
        n_str_req = 0
    n_str_pos.append(n_str_req)
print('The required number of stringers')
print(n_str_pos)

k = 18  # chord position index

str_spacing = 0.55/(max(n_str_pos) + 1) * chord()[k]
str_placing = np.arange(0.15*chord()[k], 0.7*chord()[k], str_spacing)
y_top = np.array([y_top_avg]*(max(n_str_pos)+1))*chord()[k]
y_bot = np.array([y_bottom_avg]*(max(n_str_pos)+1))*chord()[k]

print(chord()[k])
print('str_spacing', str_spacing)

plt.figure('Stringers along span')
plt.plot(n_str_pos)
plt.grid()
plt.figure('maximum stringers in tightest cross section')
plt.plot(np.asarray(Upper_sheet[0] + Lower_sheet[0] + [Upper_sheet[0][0]])*chord()[k],
         np.asarray(Upper_sheet[1] + Lower_sheet[1] + [Upper_sheet[1][0]])*chord()[k])
plt.scatter(np.asarray([Upper_sheet[0][0], Upper_sheet[0][-1], Lower_sheet[0][0], Lower_sheet[0][-1]])*chord()[k],
            np.asarray([Upper_sheet[1][0], Upper_sheet[1][-1], Lower_sheet[1][0], Lower_sheet[1][-1]])*chord()[k],
            marker='o', color='red')
plt.scatter(str_placing[1:], y_top[1:], marker='x')
plt.scatter(str_placing[1:], y_bot[1:], marker='x')
plt.plot()
plt.xlim(0.15*chord()[k],0.7*chord()[k])
plt.ylim(-0.5,0.5)
plt.grid()
plt.show()
