import matplotlib.pyplot as plt
from Wing_box_adsee import y_dist
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


"deflection with this I_yy"





"buckling"



