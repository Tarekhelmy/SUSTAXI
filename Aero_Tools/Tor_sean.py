from Wing_Calculator import chord, rho, v, surfacewing
import numpy as np


"Tor sean"
C_m = -0.639
T = C_m * 0.5 * rho * v * v * surfacewing * chord()
print(T)
