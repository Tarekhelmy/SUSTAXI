from Estimations import Aircraft
from cg_calculator import CenterOfGravity
from Wing_Power_Loading import WingAndPowerSizing
from V_n_diagram import VNDiagram
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
plt.rcParams['text.usetex'] = True

class Stability(CenterOfGravity,VNDiagram):
    def __init__(self):
        super(Stability, self).__init__()
        self.script()
        self.x_ac = (0.25*self.mac + self.lemac)
        self.Vh_V = 1
        self.CLw_alpha = self.CL(self.AR)
        self.CLh_alpha = self.CL(5,self.Vh_V)
        self.difference_constraint = 0
        self.min_difference = 0
        self.CLhmax_land = -0.35*5**(1/3)
        self.Cm_cg =self.CLhmax_land
        # self.minimum = min(self.positions)*self.meters_to_feet
        # self.maximum = max(self.positions)*self.meters_to_feet
        # self.Cm_ac = self.Cm_cg + self.CLmax_land*((self.maximum) - self.x_ac)/self.mac
        self.recursion = 0
        self.deps_dalpha = 0
        self.difference = []

    def control(self,Sh_s):
        xcg_mac = self.x_ac / self.mac - (self.Cm_ac / self.CLmax_land) + (self.CLhmax_land / self.CLmax_land) * (Sh_s) * (self.lh / self.mac) * self.Vh_V ** 2
        return ((xcg_mac*self.mac)-self.lemac)/self.mac

    def stability(self,Sh_s):
        xcg_mac = self.x_ac / self.mac + (self.CLh_alpha / self.CLw_alpha) * (1 - self.deps_dalpha) * Sh_s * (self.lh / self.mac) * (self.Vh_V) ** 2
        return ((xcg_mac*self.mac)-self.lemac)/self.mac

    def CL(self,AR,Vh_V = 1):
        self.AR = AR
        self.Mach = self.Mach * Vh_V
        self.CLcurve = (2 * np.pi * self.AR * 1.2) / (2 + np.sqrt(
            4 + (self.AR * 1.2 * np.sqrt(1 - self.Mach ** 2) / 0.95) ** 2 * (1 + 1 / (1 - self.Mach ** 2))))
        return self.CLcurve

    def scissor(self):
        self.lemac_oew_pl_fuel()
        self.positions = self.cgandplot(False)
        self.maximum= max(self.positions)*self.meters_to_feet
        self.minimum = min(self.positions)*self.meters_to_feet
        maximum = (self.maximum-self.lemac) /self.mac
        minimum = (self.minimum-self.lemac) / self.mac
        self.x_ac = (0.25*self.mac + self.lemac)
        self.Cm_ac = self.Cm_cg + self.CLmax_land*((self.maximum) - self.x_ac)/self.mac
        self.CLw_alpha = self.CL(self.AR)
        self.CLh_alpha = self.CL(5,self.Vh_V)
        self.min_difference = maximum - minimum
        Sh_S = np.linspace(0,4,40)
        Stability =self.stability(Sh_S)
        Controlability =self.control(Sh_S)
        Constraint = max(min(Sh_S[Controlability > minimum]), min(Sh_S[Stability > maximum]))
        self.difference_constraint = (self.stability(Constraint)-self.control(Constraint) )
        self.difference.append(self.difference_constraint - self.min_difference)
        if abs(self.difference[-1] )> 0.0005 and self.recursion<1000 :
            self.lemac+=0.01
            self.recursion+=1
            self.scissor()
        else:
            print('Perfect lemac positioning =',self.lemac , 'ft')
            ig, ax = plt.subplots()
            ax.plot(Stability, Sh_S, label='Neutral Point')
            ax.axhline(y=Constraint, color='red', linestyle='--', label='Optimised constraint')
            ax.axhline(y=Constraint * 1.15, color='black', linestyle='--',
                       label='Optimised constraint + 15\% safety')
            ax.plot(Controlability, Sh_S, label='Controlability')
            plt.fill_between(Stability, 0, Sh_S, alpha=0.5, color='grey')
            plt.fill_between(Controlability, 0, Sh_S, alpha=0.5, color='grey')
            plt.title('Scissor Plot')
            plt.xlim((0.2, 0.7))
            plt.ylim((0, 0.3))
            plt.xlabel(r'$x_{cg}/MAC$')
            plt.ylabel(r'$\frac{S_{h}}{S}$')
            plt.legend()
            plt.show()

    def landinggearsizing(self):
        x_oew = self.locations['oew']
        f_nlg = 0.08*(self.w_oew)
        f_mlg = 0.92*(self.w_oew)
        self.x_nlg_cg = self.cockpitlength *self.meters_to_feet
        self.x_mlg = x_oew + f_nlg*self.x_nlg_cg /f_mlg
        return None


if __name__ == "__main__":
    stability = Stability()
    stability.script()
    stability.scissor()
    stability.landinggearsizing()
    print('Nose landing gear positioning =',stability.x_nlg_cg)
    print('Main landing gear positioning =',stability.x_mlg )

