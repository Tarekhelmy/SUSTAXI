from Wing_Calculator import chord
import sympy as sy
import numpy as np
#----------------------------------------------------INPUTS aileron design
b   = 18    #m
c_r = 2.564 #m
c_t = 1.0   #m

b1 = 6.7 #m
b2 = 8   #m

c_l_alpha = 5.37
tau       = 0.2
S_ref     = 35.2
b         = 18
c_d_0     = 0.0063
da        = np.pi/9
V         = 60 #m/s
#-----------------------------------------------------PROGRAM
y = sy.Symbol("y")
chord = c_r - (c_r - c_t)/(b/2) * y

c_l_da = 2 * c_l_alpha * tau / (S_ref * b) * sy.integrate(chord*y, (y, b1, b2))
c_l_p = - 4 * (c_l_alpha + c_d_0) / (S_ref * b**2) * sy.integrate(y**2 * chord, (y, 0, b/2))

P = - c_l_da / c_l_p * da * 2 * V / b

print('Steady state roll rate:', P, 'radians per second.')
#------------------------------------------------------------