from Aero_Tools.Wing_box_adsee import y_dist
from Wing_Calculator import lift, comp_halfdata, trailingedgeangle, leadingedgeangle, c_r
import numpy as np
#print((lift()))
#print(-1*comp_halfdata[:,0])

n_safety=1.5

# ======= Materials =======
# Aluminium 7075
E_al7075 = 71.7 # GPa
UTS_al7075 = 572 # MPa
YTS_al7075 = 503 # MPa
poisson_al7075 = 0.33
G_al7075 = 26.9 # GPa
#ShS_al7075 =

def Mz():
    Mz = abs(comp_halfdata[1:,0]) * lift()
    Mn = ()
    for i in range(0,len(Mz)+1,1):
        Mn += (sum(Mz[:i]),)

    return Mn

#plt.plot(comp_halfdata[1:,0],Mz())
#plt.show()

"calculating chord at x coordinates"
def chord():
    x_coords = -comp_halfdata[1:,0]
    return c_r() - (x_coords*(np.tan(trailingedgeangle())+np.tan(leadingedgeangle())))

print(chord())
"required I_yy at each point along span"
yy = chord()*y_dist
mz = np.array(Mz())
sigma = 1.5*YTS_al7075*10**6
i_yy = mz[1:]*yy/sigma

print("required I_yy in m4 * 10^6",i_yy*10**6)

"I_yy of a single stringer"
t_string = 10
l_string = 100

# Stringers
# L-shape
L_base = 100 # mm
L_web = 100 # mm
t_str_L = 3 # mm
cent_y_str_L = (L_base * t_str_L * t_str_L/2 + L_web * t_str_L * L_web/2)/(L_base * t_str_L + L_web * t_str_L)
I_yy_str_L = t_str_L*L_web**3/12 + (L_web/2 - cent_y_str_L)**2 * L_web*t_str_L \
           + (cent_y_str_L - t_str_L/2)**2 * L_base*t_str_L

# Z-shape
Z_base = 50     # mm
Z_web = 100     # mm
Z_top = 50      # mm
t_str_Z = 3       # mm
cent_y_str_Z = Z_web/2
I_yy_str_L_Z = t_str_Z*Z_web**3/12 \
            + (cent_y_str_Z - t_str_Z/2)**2 * (Z_base + Z_top) *t_str_Z

"deflection with this I_yy"





"buckling"



