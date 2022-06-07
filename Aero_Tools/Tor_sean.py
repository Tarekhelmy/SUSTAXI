from Wing_Calculator import chord, rho, v, surfacewing
from Ben_ding import y_top_avg, y_bottom_avg
import numpy as np

A = (y_top_avg - y_bottom_avg)* (.7-.15)
Area = A * chord()*chord()
t_min = 0.003

"Tor sean"
C_m = -0.543
T = C_m * 0.5 * rho * v * v * surfacewing * chord()
q = T / (2* A)
tau_max =
