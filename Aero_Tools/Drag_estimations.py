from Wing_Calculator import surfacewing, spanb, c_t, trailingedgeangle, leadingedgeangle, c_r, AR
import numpy as np

r = 1 #m
c = c_r() -  np.tan(trailingedgeangle()) + np.tan(leadingedgeangle())
C_L = 1.5
#method 1
def meth1():
    S_Wet_wing = surfacewing + (spanb()/2-r)*(c+c_t())*0.5
    S_Wet_fuse = (5.1+3.12)*2*np.pi*r
    S_Wet_nose = np.sqrt(2.557**2 + 1**2) * np.pi * r
    S_Wet_tailcone = np.sqrt(3.76**2 +1**2) * np.pi * r
    S_Wet_tail = 4.84*2 + 5.35*2

    S_wet = S_Wet_wing + S_Wet_fuse + S_Wet_nose + S_Wet_tailcone + S_Wet_tail
    S_ref = surfacewing

    c_Fe = 0.0045

    C_D01 = c_Fe*(S_wet/S_ref)
    return C_D01 #, S_Wet_fuse+S_Wet_nose+S_Wet_tailcone+S_Wet_tail

#method 2
def meth2():
    wing = 0.007 * surfacewing
    fuselage = 0.08 * np.pi * r**2
    nacelle= 0.06 * .68 *2
    tail = 0.008*(4.84+5.35)

    C_D02 = 1.15*(wing+fuselage+nacelle+tail)

    return C_D02/surfacewing

#method 3
def meth3():
    wing = 1.07 *  (spanb()/2-r)*(c+c_t())
    tail = 1.05 * 2 * (5.35+4.84)
    D = 2
    L1 = 2.557
    L2 = 5.1+3.12
    L3 = 3.76
    A = np.pi*D / 4
    B = 1 / (3*L1**2)
    C = (4*L2**2 + (D**2) /4)**1.5 -((D**3)/8)
    E = -D +4*L2 + 2*np.sqrt(L3**2 + (D**2)/4)
    fuse = A*((B*C)+E)

    return fuse

#print(meth2(),meth1())

#print(4.84+5.35)

#drag due to lift
def D_L():
    def e(x):

        e = 1.78*(1-0.045*x**0.68)-0.64
        return e


    df = np.radians(40)
    de = 0.0046*df
    DAR = 1.9*(0.54/spanb())*AR

    #print(e(AR+DAR)+de)

    C_D = C_L**2 / (np.pi * (AR+DAR) * e(AR+DAR))
    return C_D

print(meth2(),D_L(), "total drag in cruise", meth2()+D_L())



