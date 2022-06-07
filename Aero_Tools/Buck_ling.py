import numpy as np
from Ben_ding import YTS_al7050, E_al7050, t_str_L, t_str_Z


alpha = 0.8
C_1 = 0.425
C_2 = 4
nu = 0.33
b_1 = 20 #mm
b_2 = 25 #mm
n = 0.6
t_b_1 = (t_str_Z/b_1)**2
t_b_2 = (t_str_Z/b_2)**2
Af = E_al7050*10**9 * np.pi**2 /(12*(1-(nu**2)))
Gf_1 = C_1/(YTS_al7050*10**6)
Gf_2 = C_2/(YTS_al7050*10**6)

sig_sig_13 = alpha * ((Gf_1 * Af * t_b_1)**(1-n))
sig_sig_2 = alpha * ((Gf_2 * Af * t_b_2)**(1-n))

print(sig_sig_13,sig_sig_2)


