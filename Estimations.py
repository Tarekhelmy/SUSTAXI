import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from Wing_Power_Loading import WingAndPowerSizing
import math

class Aircraft(WingAndPowerSizing):

    def __init__(self):
        super().__init__()

        self.kg_to_pounds = 2.20462
        self.meters_to_feet = 3.28084
        self.watts_to_horsepower = 0.00134102
        ##### Conversion factors ########


        #### Powertrain parameters ####
        self.n_pmad = 0.9
        self.n_fc = None
        self.n_ee = None
        self.delta_t_func = None
        self.delta_T = None
        self.T_air = None
        self.waste_heat_power = None
        self.m_comp = None
        self.m_cooling = None
        self.n_fc = None
        self.n_pmad = None
        self.n_ee = None
        self.m_fuel_cell = None
        self.fc_power = None
        self.m_pmad = None
        self.rho_pmad = 10000 * (self.watts_to_horsepower / self.kg_to_pounds)
        self.m_electric_engine = None
        self.pmad_power = None
        self.engine_power = None

        # Wing group
        self.x_wing_cg = 0
        self.x_engine_cg = 0
        self.x_battery = 0

        # Fuselage group
        self.x_fuselage_cg = 0
        self.x_fuel_cg = 0
        self.x_empennage_cg = 0
        self.x_landingGear_cg = 0
        self.x_nlg_cg = 0
        self.x_payload_cg = 0
        self.x_crew_cg = 0


        ######## Structure Masses ########
        self.m_wing = [0]
        self.m_h = 0
        self.m_v = 0
        self.m_fuselage = [0]
        self.w_design = 0
        self.w_crew = 200 * self.kg_to_pounds
        self.f_res = 0.2
        self.w_empty = 0
        self.w_installedEngine = 0
        self.w_flightcontrols = 0
        self.w_hydraulics = 0
        self.w_electrical = 0
        self.w_icing = 0
        self.w_powertrain = 0
        self.w_fuelsystem = 0
        self.w_furnishing = 0
        self.w_avionics = 1000
        self.w_battery = 0
        self.w_mtow = 0
        self.w_oew = 3500*2.25

        ########## Payload Masses ###########
        self.w_fuel = 0
        self.w_payload = 800*self.kg_to_pounds

        ######### Performance ###########
        self.L_D_cruise = self.CL_CD_cruise
        self.L_D_loiter = self.CL_CD_cruise
        self.c_p = 90 * 10**-3 * 10**-6
        self.R = 1500 * 1000
        self.V = 500 * 1000 / 3600
        self.E = self.R / self.V
        self.efficiency = 0.85
        self.CL_alpha = 0
        self.CLh_alpha = 0
        self.CLw_alpha = 0
        self.Mach = self.V/340
        self.w_s = self.find_DP()[0] / (9.81/self.kg_to_pounds*self.meters_to_feet**2)
        self.w_p = self.find_DP()[1] *self.kg_to_pounds / (9.81*self.watts_to_horsepower)

        ########## Geometrical parameters #############
        self.length_fus = [13 * self.meters_to_feet]
        self.height_fus = 1.73 * self.meters_to_feet
        self.width_fus = 1.9 * self.meters_to_feet
        self.diameter_fus = 1.9 * self.meters_to_feet
        self.lh = 5.9 * self.meters_to_feet
        self.lv = 5.4 * self.meters_to_feet
        self.t_c = 0.1

        self.fractions = 0.992 * 0.996 * 0.996 * 0.990 * 0.992 * 0.992
        self.fuel_factor = 0
        self.AR = 10
        self.sweep_angle = 30 * np.pi / 180
        self.sweep_angle_horizontal = 30 * np.pi / 180
        self.sweep_angle_vertical = 30 * np.pi / 180
        self.q = 0.5 * 1.225 * (self.V)**2 * (self.kg_to_pounds / (self.meters_to_feet**2))
        self.taper_ratio = 0.4
        self.lamda = self.taper_ratio
        self.root_chord = 2.5
        self.taper_ratio = 0.3
        self.taper_ratioh = 1
        self.taper_ratiov = 0.8
        self.mac = 1.85  # Assumed
        self.mac = self.root_chord * 2 / 3 * (1 + self.taper_ratio + self.taper_ratio ** 2) / (1 + self.taper_ratio)





        # tail volumes from https://onlinelibrary.wiley.com/doi/pdf/10.1002/9781118568101.app1


        # Mean Geometric Chord assumption

        ####### Class 1 Statistical Data ############
        self.MTOWstat = np.multiply([14330, 16424, 46500, 22900, 25700, 12500, 15245, 11300, 12500, 8200, 9850, 14500, 36000, 8500, 45000, 34720, 5732, 7054, 28660, 44000, 41000, 21165, 26000, 9000],1)
        self.OEWstat = np.multiply([7716, 9072, 26560, 14175, 16075, 7750, 8500, 6494, 7538, 4915, 5682, 8387, 23693, 4613, 25525, 20580, 3245, 4299, 16094, 27000, 24635, 11945, 15510,  5018],1)
        self.subsystem_weightage = dict()
        self.subsystem_weightage = {'fuselage': 10 ,'wing':8 , 'tail':1.3 ,'undercarriage':4.5 , 'nacelle':3 , 'engines': 9}
        self.a = linregress(self.MTOWstat, self.OEWstat).slope
        self.b = linregress(self.MTOWstat, self.OEWstat).intercept
        self.iter = 0
        self.ult_factor = 1.5
        self.length_mlg = 0.6
        self.length_nlg = 0.5
        self.n_passengers = 6
        self.shaft_power = 0
        self.fuel_volume = 0
        self.change = 0
        self.limit_load = 2.5
        self.limit_factor = 1.5
        self.specific_power_engine = 2000 * self.watts_to_horsepower / self.kg_to_pounds
        self.surface_wing = self.w_mtow / self.w_s
        self.b_w = np.sqrt(self.AR * self.surface_wing)
        self.electric_net = 0
        self.vertical_volume = 0.03 * (self.surface_wing * self.b_w + 10*self.height_fus**2*self.length_fus[-1])
        self.horizontal_volume = 0.2 * (self.surface_wing * self.mac+ 2*self.width_fus**2*self.length_fus[-1])*(self.AR+2)/(self.AR-2)
        self.surface_controlv = self.vertical_volume / self.lv
        self.surface_controlh = self.horizontal_volume / self.lh

        self.component_matrix = []


    def class1(self):
        cruise_fraction = np.exp(self.R*(9.81*self.c_p)/(self.efficiency*self.L_D_cruise))
        f1 = 1/cruise_fraction
        loiter_fraction = np.exp(self.E*(9.81*self.c_p)/(self.V*self.L_D_loiter))
        f2 = 1/loiter_fraction
        if self.iter>1:
            self.w_fuel = self.fuel_factor * (1 + self.f_res) * self.w_mtow*40/120
            self.w_oew = self.w_mtow - self.w_fuel - self.w_payload
            self.surface_wing = self.w_mtow / self.w_s
            self.b_w = np.sqrt(self.AR * self.surface_wing)
        else:
            self.fuel_factor = 1-(f1*f2*self.fractions)
            self.w_mtow = (self.w_payload + self.b + self.w_crew) / (1 - self.a - self.fuel_factor * (1 + self.f_res)*40/120)
            self.w_fuel = self.fuel_factor * (1 + self.f_res) * self.w_mtow*40/120
            self.w_oew = self.w_mtow - self.w_fuel - self.w_payload
            self.surface_wing = self.w_mtow / self.w_s
            self.b_w = np.sqrt(self.AR * self.surface_wing)

    def powertrain_mass(self):

        """
        Parameters:
            n_em [x]
            n_fc [x]
            n_pmad [v]
            PR_comp [x] this week
            n_comp p[x] this week
            rho_comp [x]
            rho_pmad [v]
            rho_em [x]
            rho_fc [x]


        1. Get Shaft Power - DONE
        2. Calculate Electric power to produce
           The required shaft power. -- EM efficiency
        2.a. get EM specific power [W/kg]
        3. Get the efficiency of the PMAD system
        4. Calculate Compressor power
        5. Calculate cooling power
        6. Calculate FC efficiency & specific power
        7.


        """
        # All power values in --> hp?? <--
        self.shaft_power = self.w_mtow / self.w_p # CONNECT!!!  # convert to kg
        self.electric_net = self.shaft_power / self.n_ee
        self.m_electric_engine = self.engine_power / 5 # engine power: [kW]
        self.pmad_power = self.engine_power / self.n_pmad
        self.m_pmad = self.pmad_power / self.rho_pmad

        self.fc_power = self.pmad_power / self.n_fc
        self.m_fuel_cell = self.fc_power / 2
        self.waste_heat_power = (1 / self.n_fc - 1) * self.fc_power

        self.delta_t_func = 0.0038 * (self.T_air / self.delta_T) ** 2 + 0.0352 * (self.T_air / self.delta_T) + 0.1817
        self.delta_t_func = None
        self.m_cooling = (0.194 * self.waste_heat_power + 1.39) * self.delta_t_func
        self.m_comp = None

        self.w_installedEngine = 1.2 * (self.m_electric_engine + self.m_fuel_cell + self.m_pmad + self.m_cooling + self.m_comp)

    def class2(self):

        self.w_design = self.w_oew - self.w_crew
        Ht_Hv = 1
        ###### Link for mass estimations used #######

        ###### https://www.ijemr.net/DOC/AircraftMassEstimationMethods(170-178).pdf ######
        ###### https://brightspace.tudelft.nl/d2l/le/content/419892/viewContent/2368629/View ######  <--- all raymer formulas

        ###### Fuselage mass ######

        self.pressurised_volume = self.diameter_fus**2*np.pi*self.length_fus[-1]/4
        self.m_fuselage.append(0.052*(self.length_fus[-1]*self.diameter_fus*np.pi)**1.086*(self.w_design*self.limit_load*self.limit_factor)**0.117*self.lh**(-0.051)*(self.CL_CD_cruise)**(-0.072)*self.q**0.241+11.9+(self.pressurised_volume*8)**0.271)

        ###### Main Wing mass ######

        # self.m_wing.append(0.0051*(self.w_design*1.5*2.5)**(0.557)*self.surface_wing**
        #               0.649*self.AR**0.5*(self.t_c)**(-0.4)*(1+self.lamda)**0.1*
        #               (np.cos(self.sweep_angle))**(-1)*(self.surface_controlv+self.surface_controlh)**0.1)

        self.m_wing.append(0.036*self.surface_wing**(0.758)*(800*2.208)**0.0035*(self.AR/(np.cos(self.sweep_angle)**2))**0.6*self.q**(0.006)*self.taper_ratio**0.04*(100*self.t_c/(np.cos(self.sweep_angle)))**-0.3*(self.limit_factor*self.limit_load*self.w_design)**0.49)

        ###### Horizontal stabilizer mass ######

        self.m_h = 0.016*(self.limit_factor*self.limit_load*self.w_design)**0.414*self.q**(0.168)*self.surface_controlh**(0.896)*\
                 (100*self.t_c/np.cos(self.sweep_angle_horizontal))**(-0.12)

        ###### Vertical stabilizer mass######

        self.m_v = 0.073*(1+0.2*(Ht_Hv))*(1.5*2.5*self.w_design)**0.376*self.q**0.122*self.surface_controlv**(0.873)*\
                   (100*self.t_c/(np.cos(self.sweep_angle_vertical)))**(-0.49)*\
                   (self.AR/(np.cos(self.sweep_angle_vertical)**2))**(0.357)*(self.taper_ratiov)**0.039  #checked

        ###### Powertrain mass ######
        # All power values in --> kW <--
        self.shaft_power = self.w_mtow / self.w_p # CONNECT!!!  #convert to kg
        # self.engine_power = self.shaft_power / self.n_ee
        # self.m_electric_engine = self.engine_power / 5 # engine power: [kW]
        # self.pmad_power = self.engine_power / self.n_pmad
        # self.m_pmad = self
        # .pmad_power / 10
        # self.fc_power = self.pmad_power / self.n_fc
        # self.m_fuel_cell = self.fc_power / 2
        # self.waste_heat_power = (1 / self.n_fc - 1) * self.fc_power
        #
        # self.delta_t_func = 0.0038 * (self.T_air / self.delta_T) ** 2 + 0.0352 * (self.T_air / self.delta_T) + 0.1817
        # self.delta_t_func = None
        # self.m_cooling = (0.194 * self.waste_heat_power + 1.39) * self.delta_t_func
        # self.m_comp = None
        #
        # self.w_installedEngine = 1.2 * (self.m_electric_engine + self.m_fuel_cell + self.m_pmad + self.m_cooling + self.m_comp)

        # Reference Formula from Raymer:

        self.w_engine = self.w_mtow / self.w_p / self.specific_power_engine

        ###### Installed Engine mass#######

        self.w_installedEngine = 2.575 * 2 * self.w_engine**0.922

        ###### Landing Gear Group mass#####

        self.m_mlg = 0.095 * (self.ult_factor * self.w_mtow) ** 0.768 * (self.length_mlg / 12) ** 0.409
        self.m_nlg = 0.125 * (self.ult_factor * self.w_mtow) ** 0.566 * (self.length_nlg / 12) ** 0.845

        ###### Fuel System mass #######

        #self.w_fuelsystem =  400  # self.shaft_power / 2  COMPLETE FORMULA
        # Reference Formula from Raymer :

        ###### Flight controls mass ######

        self.w_flightcontrols = 0.053 * self.length_fus[-1]**(1.536) * self.b_w ** (0.371) * (self.limit_factor*self.limit_load*self.w_design*10e-4)**0.8

        ###### hydraulics mass ######

        self.w_hydraulics = 0.001 * self.w_design # checked

        ###### Electrical system mass ######

        self.w_electrical = 12.57 * (self.w_fuelsystem+self.w_avionics) ** 0.51 # checked

        ###### Avionics mass ######

        self.w_avionics = 2.177*800**0.933  # fine

        ###### AC and Icing mass #######

        self.w_icing = 0.265 * self.w_design ** 0.52 * self.n_passengers**0.68 * self.w_avionics ** 0.07 * self.Mach * 0.08 # checked

        ###### Furnishing mass #######

        self.w_furnishing = 0.0582 * self.w_design - 65 # checked

        ###### updating OEW ########

        self.w_fuel = self.w_fuel *self.oew()/self.w_oew
        self.fuel_volume = self.w_fuel*2.8 / (71 * self.kg_to_pounds / (self.meters_to_feet ** 3))
        self.w_fuelsystem = 2.49*self.fuel_volume**0.726*(1/(1+1.1))**0.363*2**0.242*2**0.157  # self.shaft_power / 2  COMPLETE FORMULA


        self.w_oew = (self.m_fuselage[-1] + self.m_h + self.m_v + self.m_wing[-1] + self.w_furnishing +
                     self.w_icing + self.w_electrical + self.w_avionics + self.w_fuelsystem
                     + self.w_flightcontrols + self.w_installedEngine + self.w_hydraulics) # checked

        ###### updating MTOW ########
        self.w_mtow = self.w_oew +self.w_payload + self.w_fuel # ch

        self.iter += 1


    def oew(self):
        oew = (self.m_fuselage[-1] + self.m_h + self.m_v+ self.m_wing[-1]+ self.w_furnishing +
         self.w_icing + self.w_electrical + self.w_avionics + self.w_fuelsystem
         + self.w_flightcontrols + self.w_installedEngine + self.w_hydraulics)
        return oew

    def mtow(self):
        mtow = self.oew() + self.w_fuel + self.w_payload
        return mtow

    def print_length(self, parameter):
        print('%.2f' % (parameter / self.meters_to_feet), ' m')

    def print_mass(self, parameter):
        print('%.2f' % (parameter / self.kg_to_pounds), ' kg' )

    def print_power(self, parameter):
        print('%.2f' % (parameter / 1000 * self.watts_to_horsepower), ' kW')

    def mainsizing(self):

        self.fuel_volume = self.w_fuel / (71 * self.kg_to_pounds / (self.meters_to_feet**3))
        print('Fuel volume = ',self.fuel_volume)
        self.length_fus.append(self.length_fus[-1] + self.fuel_volume / ((self.diameter_fus)**2 * np.pi / 4))
        self.x_fuselage_cg = self.length_fus[-1] / 2
        self.x_fuel_cg = self.length_fus[-1] - 0.5 * self.fuel_volume / ((self.diameter_fus-0.14)**2 * np.pi / 4)
        self.change = (self.length_fus[-1] / self.length_fus[-2]) * self.subsystem_weightage['fuselage']/100 + (1-self.subsystem_weightage['fuselage']/100)
        self.m_fuselage.append(self.change * self.m_fuselage[-1])
        self.m_wing.append(self.m_wing[-1] * self.change)
        self.change = self.oew() / self.w_oew
        self.surface_wing = self.w_mtow / self.w_s
        #self.surface_wing = self.surface_wing * self.change
        # if (self.oew()-self.w_oew) / self.w_oew >= 0.07:
        #     self.change = self.oew() / self.w_oew
        #     self.w_oew = self.oew()
        #     self.w_fuel = self.w_fuel * self.change
        #     self.w_mtow = self.mtow()
        #
        #     self.mainsizing()

        pass

    def classiter(self):

        # print('-----------------')
        # print('iteration ', self.iter)
        self.class1()
        OEW1 = self.w_oew
        # print('OEW c1 = ', OEW1*0.45, 'kg' )
        self.class2()
        OEW2 = self.w_oew
        # print('OEW c2 = ', OEW2*0.45 , 'kg')
        # self.mainsizing()
        # print('Wing Area = ', self.surface_wing/(3.28**2), 'm^2')

        # plot all the masses
        # self.printing()
        mass_vec = np.array([self.m_fuselage[-1], self.m_h, self.m_v, self.m_wing[-1], self.w_furnishing, self.w_icing,
            self.w_electrical, self.w_avionics, self.w_fuelsystem, self.w_flightcontrols, self.w_installedEngine, self.w_hydraulics])
        self.component_matrix.append(mass_vec)

        if np.abs(OEW2 - OEW1)/OEW2 >= 0.01:
            if self.iter <= 500:
                self.classiter()



    def printing(self):

        print('-------')
        print('fuse length ',self.length_fus[-1] * 0.3048)
        print('fuse mass ',self.m_fuselage[-1]/self.kg_to_pounds)
        print('fuse diam',self.diameter_fus * 0.3048)
        print('design weight',self.w_design / self.kg_to_pounds )
        print('lh',self.lh * 0.3048)
        print('cl/cd cruise',self.CL_CD_cruise)
        print('dyn pressure',self.q / (self.kg_to_pounds * self.meters_to_feet))
        print('pressurized volume',self.pressurised_volume * 0.3048 ** 3)

        print('fuel system mass', self.w_fuelsystem)
        print('--------')
        print(self.w_p *9.81 /self.kg_to_pounds *self.watts_to_horsepower)
        print('Power  = ',self.w_mtow/self.w_p/self.watts_to_horsepower , 'W')
        print('MTOW = ', self.w_mtow/self.kg_to_pounds , 'kg')
        print('OEW Mainsizing = ', self.w_oew*0.45 , 'kg')
        print('Wing Area = ', self.surface_wing/(3.28**2), 'm^2')

    def plot_mass_progression(self):
        labels = ['fuselage', 'horizontal stab', 'vertical stab', 'wing', 'furnishing', ' de-icing', ' electronics', 'avionics', ' fuelsystem', ' flightcontrols',  'engine', ' hydraulics']
        self.component_matrix = np.array(self.component_matrix).transpose()
        # print(self.component_matrix)

        for i in range(1,13):
            x = range(self.iter)
            y = self.component_matrix[i-1]
            # c1 = math.ceil(i / 6) - 1
            # c2 = math.ceil((i - c1 * 6) / 3) - 1
            plt.figure()
            plt.plot(x, y, label=labels[i-1])
            plt.legend()
            plt.show()
            # lol = input("something : ")

    def cg_lists(self):

        self.classiter()
        self.mainsizing()

        weights = {"fuselage": self.m_fuselage[-1], "empennage": self.m_h + self.m_v, "mlg": self.m_mlg, "nlg": self.m_nlg, "crew": self.w_crew, "wing": self.m_wing[-1], "battery": self.w_battery, "engine": self.w_installedEngine, "fuelsystem": self.w_fuelsystem, "mtow": self.w_mtow, "oew": self.w_oew, "payload": self.w_payload, "fuel": self.w_fuel}
        fuselage_cg = {"fuselage": self.x_fuselage_cg, "empennage": self.x_empennage_cg, "mlg": self.x_landingGear_cg, "nlg": self.x_nlg_cg, "crew": self.x_fuselage_cg, "fuelsystem": self.x_fuel_cg, "payload": self.x_payload_cg, "fuel": self.x_fuel_cg}
        wing_cg = {"wing": self.x_wing_cg, "battery": self.x_battery, "engine": self.x_engine_cg}
        mac = self.mac
        return weights, fuselage_cg, wing_cg, mac

    def landinggearsizing(self):


        pass

    def empennagesizing(self):


        pass

aircraft = Aircraft()
aircraft.classiter()
aircraft.mainsizing()
aircraft.printing()
# aircraft.plot_mass_progression()
