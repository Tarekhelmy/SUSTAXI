import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['text.usetex'] = True


x = [1,3,5,7,9,11,13,15]
n_p = np.multiply([0.013420614084818991,0.037511296277097705,0.06320748482783295,0.07983346594833009,0.09444223334239076,0.10841280783974855,0.1240599964259057,0.14312056883526011],100)
CLmax_clean = np.multiply([0.022862234357353253,0.022862234357353253,0.014891554163825269,0.014610750892404588,0.012656355137085245,0.012656355137085245,0.012656355137085245,0.012656355137085245],100)
c = np.multiply([0.010363934894777107,0.03615675423640418, 0.053259737329656914,0.0674704638709732,0.07980775817546866,0.09143241758679362,0.10342498784713197,0.11733170971276208],100)
CL_CD_cruise = np.multiply([0,0.024860934435973894,0.024421964134227814,0.02890658533900413,0.030878649515267708,0.03110871692440051,0.030185719691015925,0.029416979020014458],100)
clean_stall_speed = np.multiply([0,0.019457594601476797,0.017859912190829413,0.01753780433814263,0.013866932768447816,0.013866932768447816,0.013866932768447816,0.013866932768447816],100)
AR = np.multiply([0,0,0.010756896856401403,0.013695610883383953,0.01603822320303904,0.018031425243205768,0.01989647922233898,0.022514636417140903],100)
Oswald_TO = np.multiply([0,0,0.010584347785137421,0.013650864190134325,0.01625070703155163,0.02321441215826801,0.0212898389624362,0.026637071424360035],100)
Cruise_altitude = np.multiply([0,0,0, 0.013433280890453167,0.01801798723772418,0.023870686380326064,0.03259045788448832,0.045800314592950926],100)


fig, axs = plt.subplots(4,2,tight_layout=True)


axs[0,0].plot(x,n_p,label = r"$\eta_{p}$")
axs[0,0].set_xlabel(r'$\eta_{p}$ percentage change', fontsize=10)
axs[0,0].set_ylabel(r'OEW percentage change', fontsize=10)

axs[1,0].plot(x,CLmax_clean,label =r'$CL_{max}_cr$')
axs[1,0].set_xlabel(r'$CL_{max}$ percentage change', fontsize=10)
axs[1,0].set_ylabel(r'OEW percentage change', fontsize=10)

axs[2,0].plot(x,c,label ='c')
axs[2,0].set_xlabel(r'c percentage change', fontsize=10)
axs[2,0].set_ylabel(r'OEW percentage change', fontsize=10)
# axs[2,0].legend()

axs[3,0].plot(x,CL_CD_cruise,label =r'$\frac{C_L}{C_D}_{cruise}$')
axs[3,0].set_xlabel(r'$\frac{C_L}{C_D}_{cruise}$ percentage change', fontsize=10)
axs[3,0].set_ylabel(r'OEW percentage change', fontsize=10)
# axs[3,0].legend()

axs[0,1].plot(x,clean_stall_speed,label =r'$V_{stall}$')
axs[0,1].set_xlabel(r'$V_{stall}$ percentage change', fontsize=10)
axs[0,1].set_ylabel(r'OEW percentage change', fontsize=10)
# axs[0,1].legend()

axs[1,1].plot(x,AR,label ='AR')
axs[1,1].set_xlabel(r'$AR$ percentage change', fontsize=10)
axs[1,1].set_ylabel(r'OEW percentage change', fontsize=10)
# axs[1,1].legend()

axs[2,1].plot(x,Oswald_TO,label =r'$e_{TO}$')
axs[2,1].set_xlabel(r'$e_{TO}$ percentage change', fontsize=10)
axs[2,1].set_ylabel(r'OEW percentage change', fontsize=10)
# axs[2,1].legend()

axs[3,1].plot(x,Cruise_altitude,label =r'$h_{cruise}$')
axs[3,1].set_xlabel(r'$h_{cruise}$ percentage change', fontsize=10)
axs[3,1].set_ylabel(r'OEW percentage change', fontsize=10)
# axs[3,1].legend()
# axs[0,0].title('lol')
# axs[1,0].title('lol2')

plt.show()
