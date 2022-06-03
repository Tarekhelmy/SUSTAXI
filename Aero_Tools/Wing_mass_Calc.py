from Wing_Calculator import trailingedgeangle, leadingedgeangle, spanb, c_r, comp_halfdata
from Wing_box_adsee import wing_box
import math as mt
import numpy as np

"""
t_upper = 0.002
t_lower = 0.002
t_le = 0.005    
t_te = 0.005
"""

def mass_wingbox(t_up, t_low, t_le, t_te, rho):


    I_yy_box, Upper_sheet, Lower_sheet = wing_box(0.15, 0.7)

    def chord_wmc():
        z_coords = abs(comp_halfdata[:,0])
        return c_r() - z_coords*mt.tan(trailingedgeangle()) - z_coords*mt.tan(leadingedgeangle())


    "calculating upper dist using pietje"
    Up_x = np.array(Upper_sheet[0])
    Up_y = np.array(Upper_sheet[1])
    dx_up = np.square(Up_x[1:-1]-Up_x[2:])
    dy_up = np.square(Up_y[1:-1]-Up_y[2:])
    dist_up = np.sqrt(dx_up+dy_up)

    "calculating lower dist using pietje"
    Low_x = np.array(Lower_sheet[0])
    Low_y = np.array(Lower_sheet[1])
    dx_low = np.square(Low_x[1:-1]-Low_x[2:])
    dy_low = np.square(Low_y[1:-1]-Low_y[2:])
    dist_low = np.sqrt(dx_low+dy_low)

    def M_sheet(dist,t):
        b= []
        for i in range(0,len(chord_wmc()),1):
            b.append(chord_wmc()[i]*dist)
        ab = np.array(b)

        z_dist=abs(comp_halfdata[:-1,0]) - abs(comp_halfdata[1:,0])
        area_top = []
        abc = ab[1:]

        for i in range(0,len(z_dist),1):
            area_top.append(abc[i]*z_dist[i])
        mass = np.sum(area_top)*rho*t
        return mass

    print(M_sheet(dist_low,t_low),M_sheet(dist_up,t_up))

    Fr_spar = Up_y[0]-Low_y[0]
    Re_spar = Up_y[-1]-Low_y[-1]

    tip_fr_spar = chord_wmc()[0]*Fr_spar
    root_fr_spar = chord_wmc()[-1]*Fr_spar
    fr_spar_area = 0.5*(tip_fr_spar+root_fr_spar)*spanb()/2

    tip_re_spar = chord_wmc()[0]*Re_spar
    root_re_spar = chord_wmc()[-1]*Re_spar
    re_spar_area = 0.5*(tip_re_spar+root_re_spar)*spanb()/2

    def M_spar(area,t):
        mass = area*rho*t
        return mass



    return M_spar(re_spar_area,t_te) + M_spar(fr_spar_area,t_le) + M_sheet(dist_low,t_low) + M_sheet(dist_up,t_up)

print(mass_wingbox(0.003,0.003,0.008,0.008,2700))