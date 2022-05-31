import matplotlib.pyplot as plt
#from Wing_box_adsee import x_mid, y_mid, wing_box
from Wing_Calculator import lift, comp_halfdata, trailingedgeangle, leadingedgeangle, c_r
import numpy as np
#print((lift()))
#print(-1*comp_halfdata[:,0])

def Mz():
    Mz = abs(comp_halfdata[1:,0]) * lift()
    Mn = ()
    for i in range(0,len(Mz),1):
        Mn += (sum(Mz[:i]),)

    return Mn

#plt.plot(comp_halfdata[1:,0],Mz())
#plt.show()

"calculating chord at x coordinates"
def chord():
    x_coords = -comp_halfdata[:,0]
    return c_r() - (x_coords*(np.tan(trailingedgeangle())+np.tan(leadingedgeangle())))

print(chord())
"required I_yy at each point"


# ======= Materials =======
# Aluminium 7075
E_al7075 = 71.7 # GPa
UTS_al7075 = 572 # MPa
YTS_al7075 = 503 # MPa
poisson_al7075 = 0.33
G_al7075 = 26.9 # GPa
ShS_al7075 =