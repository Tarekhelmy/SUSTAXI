try:
    from cg_calculator import CenterOfGravity
except ModuleNotFoundError:
    from Aircraft_simulation.cg_calculator import CenterOfGravity
# from V_n_diagram import VNDiagram
import numpy as np
import matplotlib.pyplot as plt
import csv

class Stability(CenterOfGravity):
    def __init__(self):
        super(Stability, self).__init__()
        self.script()
        self.x_ac = (0.25*self.mac + self.lemac)
        self.Vh_V = 1
        self.CLw_alpha = self.CL(self.AR)
        self.CLh_alpha = self.CL(5,self.Vh_V)
        self.mu1 = 0.17
        self.mu2 = 0.65
        self.mu3 = 0.058
        self.difference_constraint = 0
        self.min_difference = 0
        self.CLhmax_land = -0.35*5**(1/3)
        self.Cm_cg =self.CLhmax_land
        self.Cm0 = -0.0792
        self.new = self.surface_controlh
        self.previous = self.surface_controlh

        self.plot_surface = []
        self.progression= []
        self.recursion = 0
        self.deps_dalpha = 0
        self.convergenceiter = 0
        self.difference = []
        self.iterations = 0
        self.vertical_pos = 0

    def control(self,Sh_s):
        xcg_mac = self.x_ac - (self.Cm_ac / self.CLmax_land) + (self.CLhmax_land / self.CLmax_land) * (Sh_s) * (self.lh / self.mac) * self.Vh_V ** 2
        return xcg_mac

    def stability(self,Sh_s):
        xcg_mac = (self.x_ac)  + (self.CLh_alpha / self.CL_ah_alpha) * (1 - self.deps_dalpha) * Sh_s * (self.lh / self.mac) * (self.Vh_V) ** 2 -0.05
        return xcg_mac

    def CL(self,AR,Vh_V = 1):
        self.Mach = self.Mach * Vh_V
        self.CLcurve = (2 * np.pi * AR * 1.2) / (2 + np.sqrt(
            4 + (AR * 1.2 * np.sqrt(1 - self.Mach ** 2) / 0.95) ** 2 * (1 + 1 / (1 - self.Mach ** 2))))
        return self.CLcurve

    def exception(self,funcname):
        try:
            funcname()
        except ValueError:
            self.lemac+=0.1
            self.exception(funcname)

    def scissor(self, plot=False):
        global Constraint
        self.positions = self.cgandplot(True)
        self.maximum= max(self.positions)*self.meters_to_feet
        self.minimum = min(self.positions)*self.meters_to_feet
        maximum = (self.maximum-self.lemac) /self.mac
        minimum = (self.minimum-self.lemac) / self.mac
        self.Cm_ac_w = -self.Cm0*self.AR*np.cos(self.sweep_angle)**2/(self.AR+2*np.cos(self.sweep_angle))
        self.CLw_alpha = self.CL(self.AR)
        self.CL_ah_alpha = self.CLw_alpha*(1+2.15*self.diameter_fus/self.b_w)*self.surface_wing/(self.root_chord*self.diameter_fus+self.surface_wing)+np.pi*self.diameter_fus**2/(2*self.surface_wing)
        self.Cm_ac_f = -1.8*(1-2.5*self.diameter_fus/self.length_fus[-1])*(np.pi*(self.diameter_fus*self.diameter_fus*self.length_fus[-1])/(self.surface_wing*4*self.mac)*0.9*0.3423/self.CL_ah_alpha)
        self.x_ac = (0.25) - 1.8 *self.diameter_fus*self.diameter_fus*(self.lemac-0.2*self.mac)/(self.CL_ah_alpha*self.surface_wing*self.mac) + 0.273*self.diameter_fus*(self.b_w - self.diameter_fus)*self.surface_wing/self.b_w *np.tan(self.sweep_angle)/((1+self.taper_ratio)*self.mac**2*(self.b_w+2.15*self.diameter_fus))
        self.Cm_l_4 = self.mu2*(-self.mu1*1.3*1.15-(self.CLmax_land+1.3*(1-0.42))*1.15*0.15*1/8)+0.7*self.AR*self.mu3*1.3*np.tan(self.sweep_angle)/(1+2/self.AR) - self.CLmax_land*(0.25-self.x_ac)
        self.Cm_ac_flaps = self.Cm_l_4 - self.CLmax_land*(0.25-(self.x_ac))
        self.Cm_ac = self.Cm_ac_w +self.Cm_ac_f +self.Cm_ac_flaps
        self.CLh_alpha = self.CL(5,self.Vh_V)
        self.min_difference = maximum - minimum
        Sh_S = np.linspace(0,2,400)
        Stability = self.stability(Sh_S)
        Controlability = self.control(Sh_S)
        try :
            Constraint = max(min(Sh_S[Controlability > minimum]), min(Sh_S[Stability > maximum]))
            self.difference_constraint = (self.stability(Constraint)-self.control(Constraint))
            self.difference.append(self.difference_constraint-self.min_difference)
            if abs(self.difference[-1]) > 0.05 and self.recursion < 1000:
                self.lemac -= 0.1
                self.recursion += 1
                self.scissor()
        except ValueError:
            self.lemac -= 0.1
            self.scissor()
        self.surface_controlh = Constraint * 1.15 *self.surface_wing

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
            plt.ylim((0, 0.4))
            plt.xlabel(r'$x_{cg}/MAC$')
            plt.ylabel(r'$\frac{S_{h}}{S}$')
            plt.legend()
            plt.show()
            plt.savefig("scissor plot")

    def convergence(self):
        self.reset()
        self.surface_controlh = self.new
        self.mainprocedures()
        self.script()
        self.previous = self.surface_controlh
        self.lh = self.length_fus[-1] - self.locations['oew']
        self.scissor()
        self.progression.append(self.oew()/self.kg_to_pounds)
        self.new = self.surface_controlh
        self.plot_surface.append(self.surface_controlh)
        if abs(self.previous - self.new) >= 0.001:
            self.iterations +=1
            self.lemac = self.cockpitlength + 0.5 * (self.payloadlength + self.fuel_length)  # ft
            self.convergence()
        else:
            self.scissor()

    def convergenceattr(self,attr):
        # self.reset()
        self.surface_controlh = self.new
        self.mainprocedures()
        self.script()
        self.previous = self.surface_controlh
        self.lh = self.length_fus[-1] - self.locations['oew']
        self.scissor()
        self.progression.append(self.oew()/self.kg_to_pounds)
        self.new = self.surface_controlh
        self.plot_surface.append(self.surface_controlh)
        if abs(self.previous - self.new) >= 0.001:
            self.iterations +=1
            self.lemac = self.cockpitlength + 0.5 * (self.payloadlength + self.fuel_length)  # ft
            self.convergence()
        else:
            self.scissor()

    def landinggearsizing(self):
        x_oew = self.locations['oew']
        f_nlg = 0.09   # Percentage of Weight on nose landing gear
        f_mlg = 0.91   # Percentage of Weight on main landing gear
        l_nlg = x_oew - self.cockpitlength
        l_mlg = f_nlg*l_nlg/f_mlg
        self.x_nlg_cg = x_oew - l_nlg
        self.x_mlg = x_oew + l_mlg
        point1x = self.length_fus[-1]-(2.82*self.meters_to_feet)
        point1y = 0.14*self.meters_to_feet
        point2x = x_oew
        point2y = 0.5*self.diameter_fus
        x = np.linspace(0,self.length_fus[-1],1000)
        y1 = np.tan(15*np.pi / 180)*(x-point1x)+point1y
        y2 = np.tan(-75*np.pi / 180)*(x-point2x)+point2y
        diff = abs(y1-y2)
        pointy= y1[diff == min(diff)][0]
        pointx = x[diff == min(diff)][0]
        l_mlg = pointx - x_oew
        l_nlg = f_mlg*l_mlg/f_nlg
        self.vertical_pos = pointy
        self.x_nlg_cg = x_oew - l_nlg
        self.x_mlg = x_oew + l_mlg
        return None

    def plotsurface(self):
        plt.plot(self.plot_surface)
        plt.ylabel(r'$S_{H}$')
        plt.xlabel('Iteration')
        plt.title(r'Convergence of $S_{H}$ per iteration')
        plt.show()

    def plotmass(self):
        plt.plot(self.progression)
        plt.ylabel(r'$OEW$')
        plt.xlabel('Iteration')
        plt.title(r'Convergence of $OEW$ per iteration')
        plt.show()

    def procedures(self):
        self.convergence()
        self.landinggearsizing()
        self.classiter2()
        self.scissor()

    def proceduresattr(self,attr):
        self.convergenceattr(attr)
        self.landinggearsizing()
        self.classiter2()
        self.scissor()

    def printing1(self):
        print('\nOther important parameters:\n---------------')
        print('Fuselage Length =',np.round(self.length_fus[-1]/self.meters_to_feet, 2), " [m]")
        print("All the following values have the tip of the nose as reference:")
        print('Wing Lemac Position =',np.round(self.lemac/self.meters_to_feet, 2), " [m]")
        print('OEW MAX cg = ',np.round(self.maximum/self.meters_to_feet, 2), " [m]")
        print('Nose landing gear positioning =', np.round(self.x_nlg_cg/self.meters_to_feet, 2), " [m]")
        print('Main landing gear positioning =', np.round(self.x_mlg/self.meters_to_feet, 2), " [m]")
        print('Main Landing gear vertical positioning',self.vertical_pos/self.meters_to_feet, "[m]" )
        print('Tail Area ', self.surface_controlh/self.meters_to_feet**2 , ['m^2'])
        print('Tail position ', (self.lh+self.locations['oew'])/self.meters_to_feet , ['m'])
        print('wing mass',self.m_wing[-1]/self.kg_to_pounds)
        print('Max Drag is ', self.clean_stall_speed**2*(self.CD0_clean+self.CLmax_clean**2/(self.Oswald_clean*np.pi*self.AR))*0.5*self.rho*self.surface_wing/(self.meters_to_feet**2) , '[N]' )


    def Results(self):
        with open('results.csv','w') as file:
            writer = csv.writer(file)
            writer.writerow(['Weights'])
            writer.writerow(['$W_{wing}$',self.m_wing[-1]/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{fus}$',self.m_fuselage[-1]/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Vertical}$',self.m_v/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Horizontal}$',self.m_h/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Avionics}$',self.w_avionics/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Furnishing}$',self.w_furnishing/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Icing}$',self.w_icing/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Electrical}$',self.w_electrical/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{FuelSystem}$',self.w_fuelsystem/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{FlightControls}$',self.w_flightcontrols/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{InstalledEngine}$',self.w_installedEngine/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Hydraulics}$',self.w_hydraulics/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{FuelTank}$',self.w_fueltank/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Fuel}$',self.w_fuel/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Battery}$',self.w_battery/self.kg_to_pounds,'kg'])
            writer.writerow(['CG Group Positions'])
            writer.writerow(['$x_{Fus}$',self.x_fcg/self.meters_to_feet,'m'])
            writer.writerow(['$x_{Wing}$',self.x_wcg/self.meters_to_feet,'m'])
            writer.writerow(['$x_{mlg}$',self.length_mlg/self.meters_to_feet,'m'])
            writer.writerow(['$x_{nlg}$',self.length_nlg/self.meters_to_feet,'m'])
            writer.writerow(['$\\frac{x_{OEW}}{mac}$',self.oew_cg_mac/self.meters_to_feet,'m'])
            writer.writerow(['Aircraft Dimensions'])
            writer.writerow(['$l_{Fus}$',self.length_fus[-1]/self.meters_to_feet,'m'])
            writer.writerow(['$l_{FuelTank}$',self.fuel_length/self.meters_to_feet,'m'])
            writer.writerow(['$lemac$',self.lemac/self.meters_to_feet,'m'])
            writer.writerow(['Weight Groups'])
            writer.writerow(['W_{OEW}',self.w_oew/self.kg_to_pounds,'kg'])
            writer.writerow(['W_{MTOW}',self.w_mtow/self.kg_to_pounds,'kg'])
            writer.writerow(['Power Requirement'])
            writer.writerow(['P_{shaft}',self.shaft_power/self.watts_to_horsepower/1000,'KW'])
            writer.writerow(['P_{Cooling}',self.cool_power/self.watts_to_horsepower/1000,'KW'])
            writer.writerow(['P_{FC}',self.fc_power/self.watts_to_horsepower/1000,'KW'])
            writer.writerow(['P_{Waste}',self.waste_heat_power/self.watts_to_horsepower/1000,'KW'])
            writer.writerow(['P_{Compressor}',self.comp_power/self.watts_to_horsepower/1000,'KW'])
            writer.writerow(['P_{ElectricNet}',self.electric_net/self.watts_to_horsepower/1000,'KW'])
            writer.writerow(['Power Mass distribution'])
            writer.writerow(['$W_{FuelCell}$',self.m_fuel_cell/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Cooling}$',self.m_cooling/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{Compressor}$',self.m_comp/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{PMAD}$',self.m_pmad/self.kg_to_pounds,'kg'])
            writer.writerow(['$W_{ElectricEngine}$',self.m_electric_engine/self.kg_to_pounds,'kg'])
        pass

if __name__ == "__main__":
    stability = Stability()
    stability.procedures()
    stability.Results()

    # stability.plotmass()
    # stability.printing()
    stability.printing1()