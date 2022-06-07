from Ben_ding import engine, L_base, Z_base, E_al7050, YTS_al7050, poisson_al7050, dist_bottom_avg, \
    I_yy_bottom_str, I_yy_four_corner_str, n_str_pos, n_str_fin_top_lst
from Aero_Tools.Wing_box_adsee import y_dist, wing_box
from Wing_Calculator import lift, comp_halfdata, trailingedgeangle, leadingedgeangle, c_r, engine, chord
import numpy as np
import math as mt
import matplotlib.pyplot as plt

n_safety = 1.5
n_load = 4.6
n_neg_load = 1.22*1.5

def Mz_down():
    Mz_down = (abs(comp_halfdata[1:,0])+ abs(comp_halfdata[:-1,0]))/2 * (lift()-engine())*n_neg_load
    Mn_down = ()
    for i in range(0,len(Mz_down)+1,1):
        Mn_down += (sum(Mz_down[:i]),)
    return Mn_down

yy = chord()*y_dist
mz = np.array(Mz_down())
sigma = YTS_al7050/n_safety*10**6
i_yy = (mz[1:]*yy)/sigma
"scaled calculates I_yy of the sheet at every x position"
scaled = wing_box(0.15, 0.7)[0] * ((chord())**3)

"req_I_yy is the remaining I_yy that has to be satisfied with stringers"
req_I_yy = i_yy - scaled

# Downward Bending
t_lower = 0.003  # mm

section_width = chord()*(0.7-0.15) - 2*L_base*10**-3
buck_coeff = 4
crit_sheet_buck_low = buck_coeff * mt.pi**2 * E_al7050*10**9/(12*(1-poisson_al7050**2)) *(t_lower/section_width)**2
sheet_stress_low = mz[1:]*dist_bottom_avg/(wing_box(0.15,0.7)[0]*chord()**3+I_yy_four_corner_str)

w_e_lst = []
n_str_buck_lst = []
for i in range(len(crit_sheet_buck_low)):
    sheet_stress_el = sheet_stress_low[i]
    crit_sheet_buck_el = crit_sheet_buck_low[i]
    if sheet_stress_el > crit_sheet_buck_el:
        n_str_buck = 0
        while sheet_stress_el>crit_sheet_buck_el:
            #print(sheet_stress_el)
            #print(crit_sheet_buck_el)
            n_str_buck = n_str_buck + 1
            #w_e = np.sqrt(buck_coeff * mt.pi ** 2 * E_al7050 * 10 ** 9
            #              / (12 * (1 - poisson_al7050 ** 2)) * t_upper ** 2 /sheet_stress_el)
            #print(w_e)
            #n_str_buck = mt.ceil(section_width[i] / w_e - 1)

            w_e = section_width[i] / (n_str_buck + 1) - n_str_buck*Z_base*10**-3
            #print(w_e)
            sheet_stress_el = mz[i+1]*dist_bottom_avg[i]\
                              /(wing_box(0.15,0.7)[0]*chord()[i]**3 + I_yy_four_corner_str[i] + I_yy_bottom_str[i]*n_str_buck)
            #print(sheet_stress_el)
            crit_sheet_buck_el = buck_coeff * mt.pi**2 * E_al7050*10**9/(12*(1-poisson_al7050**2)) *(t_lower/w_e)**2
            #print(crit_sheet_buck_el)
    else:
        w_e = section_width[i]
        n_str_buck = 0

    n_str_buck_lst.append(n_str_buck)
    w_e_lst.append(w_e)

w_e_lst = np.asarray(w_e_lst)
n_str_buck_lst_low = np.asarray(n_str_buck_lst)
sheet_stress_wbuckstr_low = buck_coeff * mt.pi**2 * E_al7050*10**9/(12*(1-poisson_al7050**2)) *(t_lower/w_e_lst)**2

plt.figure('critical buckling w/o stringers')
plt.plot((comp_halfdata[1:,0] + comp_halfdata[:-1,0])/2, crit_sheet_buck_low)
plt.plot((comp_halfdata[1:,0] + comp_halfdata[:-1,0])/2, sheet_stress_low, ls=':')
plt.plot((comp_halfdata[1:,0] + comp_halfdata[:-1,0])/2, sheet_stress_wbuckstr_low, ls='--')
plt.grid()
plt.figure('Number of stringers due to buckling')
plt.plot((comp_halfdata[1:,0] + comp_halfdata[:-1,0])/2, n_str_buck_lst_low)
plt.grid()

#print(n_str_buck_lst_low)
#print(n_str_pos)

n_str_fin_bottom_lst = []
for j in range(len(n_str_buck_lst)):
    n_str_fin_bottom = max(n_str_pos[j], n_str_buck_lst_low[j])
    n_str_fin_bottom_lst.append(n_str_fin_bottom)
#print(n_str_fin_bottom_lst)
plt.figure('Final Stringers')
plt.plot((comp_halfdata[1:,0] + comp_halfdata[:-1,0])/2, n_str_fin_top_lst)
plt.plot((comp_halfdata[1:,0] + comp_halfdata[:-1,0])/2, n_str_fin_bottom_lst)
plt.legend(['Top', 'Bottom'])
plt.grid()
plt.show()
