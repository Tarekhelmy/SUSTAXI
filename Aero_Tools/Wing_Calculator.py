import numpy as np
import pandas as pd
import math as mt
import sympy as sy
import matplotlib.pyplot as plt
""""
class wing_calculator(Aircraft):
   
   def __init__(self,):
        super().__init__()




   def planform(self):
        super().classiter()
        super().mainsizing()
        kg_to_pounds = 2.20462

        self.w_mtow = self.w_mtow/kg_to_pounds
        self.surface_wing = (self.surface_wing/(3.28**2))


        self.b =np.sqrt(self.surface_wing*self.AR)

        return self.surface_wing, self.w_mtow, self.AR, self.b
"""

AR= 9.94
surfacewing= 27.1
w_mtow = 5403.62
tapratio = 0.374

def spanb():
    return round(np.sqrt(surfacewing*AR),3)

def c_t():
    return round((2*surfacewing/spanb())/(1+(1/tapratio)),2)

def c_r():
    return round(c_t()/tapratio,3)

print("b/2=",spanb()/2)
print("c_t=",c_t())
print("c_r=",c_r())


v = 46 #m/s
v_c = 150
rho=1.225

#data = pd.read_table("winglift_v=46_a=15vlm.txt", sep='\s+')

def data_converter():
    data = pd.read_table("winglift_v=46_a=15vlm.txt", sep='\s+')
    data = data.to_numpy()
    data = np.delete(data,obj=2,axis=1)

    return data



"create planform"

"add first and last point"
def full_data():
    firstrow= [-spanb()/2,0]
    lastrow= [spanb()/2,0]
    ful_data=np.vstack([data_converter(),lastrow])
    ful_data=np.vstack([firstrow,ful_data])


    return ful_data


ar=len(full_data())/2

if (ar %2) == 0:
    print(full_data()[ar,0], "check if x=0")
    comp_halfdata = full_data()

else:
    print("middle is added")
    data=full_data()[:int(ar),:int(ar)]
    half_data = full_data()[:int(ar)+1,:int(ar)+1]
    cl_half_data = half_data[:int(ar)+1,1]
    data_middle = [0,(cl_half_data[int(ar)]+cl_half_data[int(ar)-1])/2]
    comp_halfdata = np.vstack([data,data_middle])
    #print(comp_halfdata)

"calculating angles"
offset=0.5
def trailingedgeangle():
    return mt.atan((c_r()-c_t()-offset)/(spanb()/2))


def leadingedgeangle():
    return mt.atan(offset/(spanb()/2))

def chord():
    z_coords = (abs(comp_halfdata[1:,0])+ abs(comp_halfdata[:-1,0]))/2
    return c_r() - z_coords*mt.tan(trailingedgeangle()) - z_coords*mt.tan(leadingedgeangle())


"calculating area"
"back"
a = len(comp_halfdata)
def Sback():

    dx_data=abs(comp_halfdata[:,0])
    backarea=dx_data*(mt.tan(trailingedgeangle())*dx_data)*0.5
    S_prime=abs((backarea[:-1]-backarea[1:]))

    return S_prime

#print(Sback())

"front"
def Sfront():

    dx_data=abs(comp_halfdata[:,0])
    frontarea=dx_data*(mt.tan(leadingedgeangle())*dx_data)*0.5
    S_prime=abs((frontarea[:-1]-frontarea[1:]))

    return S_prime

#print(Sfront())

def wing_area():
    x_data = abs(comp_halfdata[:,0])
    x_data = x_data[:-1] - x_data[1:]
    return(x_data*c_r())-Sfront()-Sback()


#print(wing_area())

def lift():
    cl_data = (comp_halfdata[:-1,1] + comp_halfdata[1:,1])/2
    "multiply middle by 2"
    list_ones = [1] * (len(cl_data)-1)
    list_ones.append(2)
    cl_data = cl_data * list_ones
    lift = cl_data*wing_area()*v*v*0.5*rho

    return lift


"add engine"
def engine():
    Z_loc_eng = 2.85
    M_engine = 600 #kg
    list_zeros = [0] * (len(lift()))

    def find_nearest(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return array[idx], idx


    Z_place_eng, n = find_nearest(abs(comp_halfdata[:,0]),Z_loc_eng)
    list_zeros[n] = -M_engine*9.81

    return list_zeros

#plt.plot(((comp_halfdata[1:,0]) + (comp_halfdata[:-1,0]))/2,lift()+engine())
#plt.show()
#print(sum(lift()+engine()))
"add right half"

righthalf_data=abs(comp_halfdata[::-1])
comp_data= np.vstack([comp_halfdata,righthalf_data])
comp_data=comp_data[:,0]

rightlift=lift()[::-1]
leftlift = lift()
comp_lift = np.hstack((leftlift,rightlift))
print("total lift =", round(sum(comp_lift),2))
print("MTOW=", 9.81*w_mtow)

#print("CLmax =", sum(comp_lift)/(0.5*rho*v*v*surfacewing))


"highlift devices"
req_CL = 9.81*w_mtow/(0.5*rho*v*v*surfacewing)

cur_CL = sum(comp_lift)/(0.5*rho*v*v*surfacewing)
Delta_CL = (req_CL - cur_CL)
#print(Delta_CL*1.0)
dcl = 0.9
Swf_S = Delta_CL/(0.9*dcl*np.cos(trailingedgeangle()))

#print("s", Swf_S)
#print("required wing lift coefficient=",(1.1*(1/q)*W_S))

#plt.plot(comp_data[1:-1],comp_lift)
#plt.show()

b1 = 1.7
b2 = 6.7

y = sy.Symbol("y")
chord_h = c_r() - (c_r() - c_t())/(spanb()/2) * y
area = sy.integrate(chord_h, (y, b1, b2))

#print(area)
#print(Swf_S*surfacewing/2)

D_a0 = -10* Swf_S * np.cos(trailingedgeangle())


#print(D_a0)
