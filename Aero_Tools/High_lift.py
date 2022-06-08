from Wing_Calculator import w_mtow, rho, surfacewing, comp_lift, trailingedgeangle, c_t, c_r, spanb
import sympy as sy
import numpy as np

"highlift devices"
req_CL = 9.81*w_mtow/(0.5*rho*40.4*40.4*surfacewing)
print(req_CL)
cur_CL = sum(comp_lift)/(0.5*rho*46*46*surfacewing)
print(cur_CL)
Delta_CL = (req_CL - cur_CL) + 0.05
print(Delta_CL*1.0)
dcl = 1.3
Swf_S = Delta_CL/(0.9*dcl*np.cos(trailingedgeangle()))

#print("s", Swf_S)
#print("required wing lift coefficient=",(1.1*(1/q)*W_S))

b1 = 2.29
b2 = 6.1

y = sy.Symbol("y")
chord_h = c_r() - (c_r() - c_t())/(spanb()/2) * y
area_fl = sy.integrate(chord_h, (y, b1, b2))


print(area_fl)
print(Swf_S*surfacewing/2)