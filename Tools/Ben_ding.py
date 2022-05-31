import matplotlib.pyplot as plt

from Wing_Calculator import lift, comp_halfdata
import numpy as np
#print((lift()))
#print(-1*comp_halfdata[:,0])

def Mz():
    Mz = abs(comp_halfdata[1:,0]) * lift()
    Mn = ()
    for i in range(0,len(Mz),1):
        Mn += (sum(Mz[:i]),)

    return Mn

print(len(Mz()))
#print(len(comp_halfdata[:,0]))
plt.plot(comp_halfdata[1:,0],Mz())
plt.show()
