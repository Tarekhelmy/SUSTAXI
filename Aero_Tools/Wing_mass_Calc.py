from Wing_Calculator import trailingedgeangle, leadingedgeangle, spanb, c_r, comp_halfdata
from Wing_box_adsee import wing_box
import math as mt
import numpy as np

t_upper = 0.002
t_lower = 0.002
t_le = 0.005
t_te = 0.005

rho_al7050 = 2.7*(10**3) #[kg/m^3]

I_yy_box, Upper_sheet, Lower_sheet = wing_box(0.15, 0.7)

def chord_wmc():
    z_coords = abs(comp_halfdata[:,0])
    return c_r() - z_coords*mt.tan(trailingedgeangle()) - z_coords*mt.tan(leadingedgeangle())



Up_x = np.array(Upper_sheet[0])
Up_y = np.array(Upper_sheet[1])
dx_up = np.square(Up_x[1:-1]-Up_x[2:])
dy_up = np.square(Up_y[1:-1]-Up_y[2:])
dist_up = np.sqrt(dx_up+dy_up)

b= []
for i in range(0,len(chord_wmc()),1):
    b.append(chord_wmc()[i]*dist_up)
ab = np.array(b)

z_dist=abs(comp_halfdata[:-1,0]) - abs(comp_halfdata[1:,0])
area = []
abc = ab[1:]

for i in range(0,len(z_dist),1):
    area.append(abc[i]*z_dist[i])

print(np.sum(area))



Low_x = np.array(Lower_sheet[0])
Low_y = np.array(Lower_sheet[1])
dx_low = np.square(Low_x[1:-1]-Low_x[2:])
dy_low = np.square(Low_y[1:-1]-Low_y[2:])
dist_low = np.sqrt(dx_low+dy_low)
