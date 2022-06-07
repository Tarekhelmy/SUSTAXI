from Wing_Calculator import chord, rho, v, surfacewing, lift, engine
from Ben_ding import y_top_avg, y_bottom_avg, i_yy, A_str_L, A_str_Z, n_load, n_str_fin_top_lst
from Downwards_bending import n_str_fin_bottom_lst
import numpy as np

def Tor_sean(t_min):
    A = (y_top_avg - y_bottom_avg)* (.7-.15)
    Area = A * chord()*chord()


    "Tor sean"
    C_m = 0.561
    T = C_m * 0.5 * rho * v * v * surfacewing * chord()
    q_T = T * n_load / (2* Area)
    tau_max_T = q_T / t_min



    "shear flow due to lift"
    top_dist = chord()* y_top_avg
    bot_dist = chord()* y_bottom_avg



    B_top = np.add(np.multiply(n_str_fin_top_lst , A_str_Z/10**6),np.array([2] * len(chord())) * A_str_L/10**6)
    B_bot = np.add(np.multiply(n_str_fin_bottom_lst , A_str_Z/10**6),np.array([2] * len(chord())) * A_str_L/10**6)
    B_tot = np.add((B_bot*bot_dist),(B_top*top_dist))
    q_L = ((lift()+engine())*n_load) * B_tot / (i_yy)

    q_tot = q_L + q_T

    tau_max = q_tot /t_min

    return tau_max / 10**9

print(Tor_sean(0.003))