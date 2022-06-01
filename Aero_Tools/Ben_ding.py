from Aero_Tools.Wing_box_adsee import y_dist, wing_box
from Wing_Calculator import lift, comp_halfdata, trailingedgeangle, leadingedgeangle, c_r
import numpy as np
#print((lift()))
#print(-1*comp_halfdata[:,0])

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
    Mz = (abs(comp_halfdata[1:,0])+ abs(comp_halfdata[:-1,0]))/2 * (lift()*n_load)
    Mn = ()
    for i in range(0,len(Mz)+1,1):
        Mn += (sum(Mz[:i]),)
    return Mn




#plt.plot(comp_halfdata[1:,0],Mz())
#plt.show()

"calculating chord at x coordinates"
def chord():
    z_coords = abs(comp_halfdata[1:,0])+ abs(comp_halfdata[:-1,0])/2
    return c_r() - (z_coords*(np.tan(trailingedgeangle())+np.tan(leadingedgeangle())))


"Bending required I_yy at each point along span"
yy = chord()*y_dist
mz = np.array(Mz())
sigma = YTS_al7050/n_safety*10**6
i_yy = (mz[1:]*yy)/sigma


scaled = wing_box(0.15, 0.7)[0] * ((chord())**2)

req_I_yy = i_yy - scaled
#print(mz[1:]*yy/i_yy/10**6)
#print(mz[1:]*yy/scaled/10**6)

"buckling"

def buckling():
    C = 4
    b = 0.55
    t = 0.004 #m
    return (C*np.pi*np.pi*E_al7050/(12*(1-poisson_al7050)))*((t/b)**2)

print(buckling())

"I_yy of a single stringer"
t_string = 10
l_string = 100

# Stringers
# L-shape
L_base = 0.100 # mm
L_web = 0.100 # mm
t_str_L = 0.003 # mm
cent_y_str_L = (L_base * t_str_L * t_str_L/2 + L_web * t_str_L * L_web/2)/(L_base * t_str_L + L_web * t_str_L)
I_yy_str_L = t_str_L*L_web**3/12 + (L_web/2 - cent_y_str_L)**2 * L_web*t_str_L \
           + (cent_y_str_L - t_str_L/2)**2 * L_base*t_str_L

# Z-shape
Z_base = 0.050     # mm
Z_web = 0.100     # mm
Z_top = 0.050      # mm
t_str_Z = 0.003       # mm
cent_y_str_Z = Z_web/2
I_yy_str_L_Z = t_str_Z*Z_web**3/12 \
            + (cent_y_str_Z - t_str_Z/2)**2 * (Z_base + Z_top) *t_str_Z







"buckling"



