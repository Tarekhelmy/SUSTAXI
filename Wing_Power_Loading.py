import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
### Minimum speed, take-off distance, landing distance, climb(rate and gradient), maneuvering(turn rate/radius), max speed, max alt
"""
 Requirements that we need:

 Landing requirements
 --------------------
 --> Landing weight
 --> Approach speed VA
 --> Deceleration method used || Prolly brakes
 --> Flying qualities of the aircraft || High wing
 --> C_L_Max (including HLDs)
 
 Cruise performance
 ----------------------
 --> propeller efficiency
 --> cruise speed
 --> cruise altitude
 --> drag polar
 --> weight fraction of MTOW at cruise
 --> power fraction of P_TO at cruise

 Climb rate performance
 ----------------------
 --> climb requirement

 Climb gradient performance
 ------------------------
 --> safety margin on lift coefficient
import numpy as np

 Minimum speed   -----> 61kts
 Take off distance  ------> <1500m
 maneuvering: turn rate & radius  -----> Relavant Later
 maximum speed  ------>
 maximum altitude ----->   for now 3048m

  """

ISA_density = 1.225 #[kg/m^3]
Lambda = -0.0065
R =287
ISA_pressure = 101325
ISA_temperature = 288.15
gravity =9.81

class WingAndPowerSizing    :
    def __init__(self, MTOW):
        self.clean_stall_speed = 46.2 # [m/s]
        self.ff_stall_speed = 40.4 #[m/s]

        self.CLmax_clean = 1.5
        self.CLmax_TO = 2.0
        self.CLmax_land = 2.4
        self.MTOW = MTOW
        self.Oswald_clean = 0.78
        self.Oswald_TO = 0.83
        self.Oswald_land = 0.88
        self.CD0_clean = 0.02 # between prop and jet (ADSEE-I, lec 3 slide 15)
        self.CD0_TO = 0.0380
        self.CD0_land = 0.0730
        self.landing_fraction = 0.95
        self.ground_distance = 1500 #[m]
        self.n_p = 0.85
        self.cruise_altitude = 5000 # m
        self.AR = 10
        self.cruise_speed = 500 / 3.6
        self.rho = 1.225
        self.pressure = 101325
        self.temperature = 288.15
        self.c = 12
        self.CL_CD_TO = self.CLmax_TO/(self.CD0_TO + (self.CLmax_TO**2/(self.Oswald_TO*self.AR*np.pi)))
        self.CL_CD_cruise = self.CLmax_clean/(self.CD0_clean + (self.CLmax_clean**2/(self.Oswald_clean*self.AR*np.pi)))
        self.CL_CD_L = self.CLmax_land/(self.CD0_land + (self.CLmax_land**2/(self.Oswald_land*self.AR*np.pi)))
        self.c_V = 0.083
        self.runway_elevation = 2500
        self.W_S = None
        self.W_P = None
        self.W_S = None
        self.W_P = None


    def ISA(self,altitude):
        pressure = ISA_pressure * (1. + (Lambda * (altitude)) / ISA_temperature) ** (-gravity / (Lambda * R))
        temperature = ISA_temperature + Lambda * altitude
        rho = pressure /(temperature*R)
        return pressure,temperature,rho
        

    def landing(self):
        x = (self.CLmax_land * ISA_density * (self.ground_distance / 0.5915)) / (2 * self.landing_fraction)
        return x

    def clean_stall(self):
        return 0.5 * ISA_density * self.clean_stall_speed ** 2 * self.CLmax_clean


    def takeoff(self, W_over_S):
        sigma = self.ISA(self.runway_elevation)[2] / 1.225
        #print('sigma = %.2f' % sigma)
        CL_TO = self.CLmax_TO / (1.1 * 1.1)
        #print('take off lift coefficient = %.2f' % CL_TO)
        TOP = 570
        W_over_P = (sigma * CL_TO * TOP) / W_over_S
        return W_over_P


    def cruise(self,x):
        pressure,temperature,rho = self.ISA(self.cruise_altitude)
        y = (9/8) *  (self.n_p * (rho/ISA_density) ** (0.75) * ((self.CD0_clean * 0.5 * rho
                                                      * self.cruise_speed ** 3) / (0.8*x) +
                                                     0.8*x / (np.pi * self.AR * self.Oswald_clean *
                                                          0.5 * rho * self.cruise_speed))**-1)
        #print(rho/ISA_density)
        return y

    def climbrate(self,x):

        y = (self.n_p / (self.c + np.sqrt(x)*np.sqrt(2/ISA_density)/
                        (1.345*(self.AR*self.Oswald_TO)**(3/4)/(self.CD0_TO**(1/4)))))
        return y

    def climbgradient(self,x):
        y = self.n_p/(np.sqrt(x)*(self.c_V+self.CL_CD_TO ** -1)*np.sqrt(2/(ISA_density*(self.CLmax_TO-0.2))))
        return y

    def plot_power(self, landing, cruise):
        x_list = np.linspace(1,5000,100)
        plt.figure(1)
        plt.grid()
        if landing:
            plt.vlines(self.landing(),0,0.4, label="landing/stall constraint")
            plt.vlines(self.clean_stall(),0,0.4, label="clean stall constraint")
        if cruise:
            plt.plot(x_list, self.cruise(x_list), linestyle="solid", color="blue", label="Cruise speed constraint")
            plt.plot(x_list, self.climbgradient(x_list), linestyle="solid", color="red", label="Climb gradient constraint")
            plt.plot(x_list, self.climbrate(x_list), linestyle="solid", color="purple", label="Climb rate constraint")
            plt.plot(x_list, self.takeoff(x_list), linestyle="solid", color="orange", label="Take-off constraint")
        plt.ylim((0,0.4))
        plt.legend()
        plt.xlabel("Wing loading (W/S) [N/m^2]")
        plt.ylabel("Power loading (W/P) [N/W]")
        plt.legend()
        plt.show()
        plt.close(1)

    def find_DP(self):
        self.W_S = self.clean_stall()
        self.W_P = self.cruise(self.W_S)
        self.S = self.MTOW / self.W_S
        self.P = self.MTOW / self.W_P
        return self.W_S, self.W_P

    def print_ac_params(self):
        self.W_S,self.W_P = self.find_DP()
        print("Wing Loading = %.2f" % self.W_S, " N/m^2")
        print("Power Loading = %.3f" % self.W_P, " N/w")
        print("Wing Area = %.2f" % self.S, " m^2")
        print("Total Power = %.2f" % (self.P / 1000), " kW")

if __name__ == '__main__':
    Aircraft = WingAndPowerSizing(5500 * 9.81)
    Aircraft.plot_power(landing=True, cruise=True)
    Aircraft.print_ac_params()
