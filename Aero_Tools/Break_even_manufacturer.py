#from astropy.table import Table
#tab = Table.read('compliance_user.txt', format='latex').to_pandas()
#Table.write('test', format='latex')
import matplotlib.pyplot as plt
import numpy as np

p = 4250000 #dollars
Q   = 300  #-
inflation = 1.73

V   = 475  #km/h
W_e = 4494.73 #kg
FTA = 1    #amount of flight tests

N_eng = 2
R   = 60 #euros (general salary)
R_M = 10 #euros (manufacturing salary)

H_E = 5.18 * W_e**0.777 * V**0.894 * Q**0.163
H_T = 7.22 * W_e**0.777 * V**0.696 * Q**0.263
H_M = 10.5 * W_e**0.82 * V**0.484 * Q**0.641
H_Q = 0.133 * H_M

C_D = 48.7 * W_e**0.630 * V**1.3 * inflation
C_F = 1408 * W_e**0.325 * V**0.822 * FTA**1.21 * inflation
C_M = 22.6 * W_e**0.921 * V**0.621 * Q**0.799 * inflation
C_eng = 1000000 * inflation

print('Engineering costs:', H_E * R * inflation, 'euro')
print('Tooling costs:', H_T * R * inflation, 'euro')
print('Manufacturing costs:', H_M * R * inflation, 'euro')
print('Engineering costs:', H_Q * R * inflation, 'euro')
RDT_flyaway = (H_E * R + H_T * R + H_M *R_M + H_Q * R) * inflation + C_D + C_F + C_M + C_eng * N_eng
print('Total fly away cost:', RDT_flyaway, 'euro')

hours       = np.array([H_E*R, H_T*R, H_M*R_M, H_Q*R])
hour_labels = ["Engineering hours", "Tooling hours", "Manufacturing hours", "QH"]
#plt.pie(hours, labels=hour_labels)

#----------------------------------------------FUNCTIONS
Quantity = np.arange(1,Q,1)
H_E = 5.18 * W_e**0.777 * V**0.894 * Quantity**0.163
H_T = 7.22 * W_e**0.777 * V**0.696 * Quantity**0.263
H_M = 10.5 * W_e**0.82 * V**0.484 * Quantity**0.641
H_Q = 0.133 * H_M

C_D = 48.7 * W_e**0.630 * V**1.3 * inflation
C_F = 1408 * W_e**0.325 * V**0.822 * FTA**1.21 * inflation
C_M = 22.6 * W_e**0.921 * V**0.621 * Quantity**0.799 * inflation
RDT_flyaway = (H_E * R + H_T * R + H_M *R_M + H_Q * R) * inflation + C_D + C_F + C_M + C_eng * N_eng
plt.plot(Quantity, p*Quantity, label='revenues')
plt.plot(Quantity, RDT_flyaway, label='total costs')
plt.legend()
plt.grid()
plt.show()

