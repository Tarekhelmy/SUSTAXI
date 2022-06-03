import numpy as np
import matplotlib.pyplot as plt
#-------------------------------------------SETTING
a = 0.805   #mm
b = 0.48   #m
l_t = 3.18  #m (tank length)

#SHELL Aluminium 2219
Shell_thickness = 0.003 #m
Shell_density   = 2780  #kg/m3


#EPS foam
Foam_density   = 26   #kg/m3
Foam_lambda    = 0.02594
Foam_thickness = 0.115   #m (thickness insulation material)

#STRUCUTRE glass foam
n_position_blocks       = 4    #-
S_position_block        = 0.071   #m2
position_blocks_lambda  = 0.035
position_blocks_density = 925   #kg/m3

T_i        = -253   #Celsius (Temperature in Tank)
T_o        = 45     #Celsius (Temperature outside Tank)
T_boil_off = -249   #Celsius

liquid_fraction         = 0.9
liquid_hydrogen_density = 70.3 #kg/m3
gas_hydrogen_density    = 3.04 #kg/m3
latent_heat             = 447000 #J/kg
specific_heat_hydrogen  = 14.304*1000 #J/kg K
#------------------------------------------OUTPUT
print('Total tank diameter:', 2*a + 2*Shell_thickness + 2*Foam_thickness, 'm')
print('Total tank length:', l_t + 2*Shell_thickness + 2*Foam_thickness, 'm')

l_s = l_t - 2*b
Volume_tank  = np.pi * a**2 * l_s + 4/3 * np.pi * a**2 * b
Surface_tank = 2 * np.pi * a * l_s + 4 * np.pi * ((2*(a*b)**1.6+a**3.2)/3)**(1/1.6)
print('Surface Tank:', Surface_tank, 'm2')
print('Volume Tank:', Volume_tank, 'm3 \n')

Hydrogen_weight = Volume_tank * (liquid_fraction * liquid_hydrogen_density + (1-liquid_fraction) * gas_hydrogen_density)
print('Hydrogen weight:', Hydrogen_weight, 'kg')

Shell_weight    = Surface_tank * Shell_thickness * Shell_density
print('Shell Weight:', Shell_weight , 'kg')

Foam_weight    = Surface_tank * Foam_thickness * Foam_density
print('Foam Weight:', Foam_weight, 'kg')

Full_tank_weight    = Foam_weight + Shell_weight + Hydrogen_weight
print('Total tank Weight:', Full_tank_weight, 'kg \n')

tank_efficiency = Hydrogen_weight / (Hydrogen_weight  + Foam_weight + Shell_weight)
print('Tank efficiency:', tank_efficiency)

Structural_insulation = n_position_blocks*S_position_block/Surface_tank #Fraction of insulation replaced by aluminium for structure
#------------------------------------------BOIL OFF
T = [T_i]
time = [0]
t = 0

while T[-1] < T_boil_off:
    t = t + 1
    time.append(t)

    Qdot_foam = Foam_lambda            * Surface_tank*(1-Structural_insulation) / Foam_thickness * (T[-1] - T_o)
    Qdot_str  = position_blocks_lambda * Surface_tank*(Structural_insulation)   / Foam_thickness * (T[-1] - T_o)
    Qdot_vent = -6
    Qdot = Qdot_str + Qdot_foam + Qdot_vent
    T_new = T[-1]-Qdot/(specific_heat_hydrogen*Hydrogen_weight)
    T.append(T_new)

print('Boil off time:', time[-1] , 'seconds,' ,time[-1]/3600, 'hours')

BOR = Qdot * 5 * 3600 / (Volume_tank * liquid_hydrogen_density * latent_heat) * 100
print('Boil off rate:', BOR, '% of the total volume has been boiled off.')

plt.plot(time, T)