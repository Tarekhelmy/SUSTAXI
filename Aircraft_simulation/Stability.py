from cg_calculator import CenterOfGravity
# from V_n_diagram import VNDiagram
import numpy as np
import matplotlib.pyplot as plt


class Stability(CenterOfGravity):
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
        self.recursion = 0
        self.deps_dalpha = 0
        self.convergenceiter = 0
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
    def exception(self,funcname):
        try:
            funcname()
        except ValueError:
            self.lemac+=0.1
            self.exception(funcname)

    def scissor(self, plot=False):
        global Constraint
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
        Sh_S = np.linspace(0,2,40000)
        Stability =self.stability(Sh_S)
        Controlability =self.control(Sh_S)
        try :
            Constraint = max(min(Sh_S[Controlability > minimum]), min(Sh_S[Stability > maximum]))
            self.difference_constraint = (self.stability(Constraint)-self.control(Constraint))
            self.difference.append(self.difference_constraint - self.min_difference)
            if abs(self.difference[-1]) > 0.01 and self.recursion < 1000:
                self.lemac -= 0.1
                self.recursion += 1
                self.scissor()
        except ValueError:
            self.lemac -= 0.1
            self.scissor()
        self.surface_controlh = Constraint *1.15 *self.surface_wing

        if plot==True:
            ig, ax = plt.subplots()
            ax.plot(Stability, Sh_S, label='Neutral Point')
            ax.axhline(y=Constraint, color='red', linestyle='--', label='Optimised constraint')
            ax.axhline(y=Constraint * 1.15, color='black', linestyle='--', label='Optimised constraint + 15\% safety')
            ax.plot(Controlability, Sh_S, label='Controlability')
            plt.fill_between(Stability, 0, Sh_S, alpha=0.5, color='grey')
            plt.fill_between(Controlability, 0, Sh_S, alpha=0.5, color='grey')
            plt.title('Scissor Plot')
            plt.xlim((0.1, 0.7))
            plt.ylim((0, 0.15))
            plt.xlabel(r'$x_{cg}/MAC$')
            plt.ylabel(r'$\frac{S_{h}}{S}$')
            plt.legend()
            plt.show()
            plt.savefig("scissor plot")

    def convergence(self):
        self.script()
        self.lh = self.length_fus[-1] - self.locations['oew']
        self.scissor()
        new = self.surface_controlh
        self.classiter()
        self.convergenceiter+=1
        previous = self.surface_controlh
        # self.script()
        if abs(previous - new) >= 0.1:
            self.lemac = 25 # ft
            self.convergence()
        else:
            self.mainsizing()
            self.scissor()



    def landinggearsizing(self):
        x_oew = self.locations['oew']
        f_nlg = 0.08   # Percentage of Weight on nose landing gear
        f_mlg = 0.92   # Percentage of Weight on main landing gear
        l_nlg = x_oew - self.cockpitlength
        l_mlg = f_nlg*l_nlg/f_mlg
        self.x_nlg_cg = x_oew - l_nlg
        self.x_mlg = x_oew + l_mlg
        point1x = self.length_fus[-1]-(2.82*self.meters_to_feet)
        point1y = 0.14*self.meters_to_feet
        point2x = x_oew
        point2y = 0.5*self.diameter_fus
        x = np.linspace(0,self.length_fus[-1],100)
        y1 = np.tan(15*np.pi / 180)*(x-point1x)+point1y
        y2 = np.tan(-75*np.pi / 180)*(x-point2x)+point2y
        diff = abs(y1-y2)
        pointy= y1[diff == min(diff)][0]
        pointx = x[diff == min(diff)][0]
        l_mlg = pointx - x_oew
        l_nlg = f_mlg*l_mlg/f_nlg
        self.x_nlg_cg = x_oew - l_nlg
        self.x_mlg = x_oew + l_mlg
        return None

    def procedures(self):
        self.convergence()
        self.landinggearsizing()
        self.classiter2()
        self.printing1()
        self.scissor(plot=True)

    def printing1(self):
        print('\nOther important parameters:\n---------------')
        print('Fuselage Length =',np.round(self.length_fus[-1]/self.meters_to_feet, 2), " [m]")
        print("All the following values have the tip of the nose as reference:")
        print('Wing Lemac Position =',np.round(self.lemac/self.meters_to_feet, 2), " [m]")
        print('OEW cg = ',np.round(self.locations['oew']/self.meters_to_feet, 2), " [m]")
        print('Nose landing gear positioning =', np.round(self.x_nlg_cg/self.meters_to_feet, 2), " [m]")
        print('Main landing gear positioning =', np.round(self.x_mlg/self.meters_to_feet, 2), " [m]")

if __name__ == "__main__":
    stability = Stability()
    stability.procedures()


