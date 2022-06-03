import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from Wing_Power_Loading import WingAndPowerSizing
from fuel_cell_optimization import FuelCellSizing

class Aircraft(WingAndPowerSizing):

    def __init__(self):
        super().__init__()

        ##### Conversion factors ########

        self.pm_it = 0
        self.kg_to_pounds = 2.20462
        self.meters_to_feet = 3.28084
        self.watts_to_horsepower = 0.00134102

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
        self.x_mlg = 0
        self.x_payload_cg = 0
        self.x_crew_cg = 0


        ######## Structure Masses ########
        self.m_wing = []
        self.m_h = 0
        self.m_v = 0
        self.m_fuselage = []
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
        self.w_battery = 50 * self.kg_to_pounds # from https://www.aircraft-battery.com/search-by-your-aircraft/battery_detail/293
        self.w_mtow = 0
        self.w_oew = 3500*self.kg_to_pounds
        self.w_fueltank = 200 * self.kg_to_pounds

        ########## Payload Masses ###########
        self.w_fuel = 0
        self.w_payload = 800*self.kg_to_pounds

        ######### Performance ###########
        self.L_D_cruise = self.CL_CD_cruise
        self.L_D_loiter = self.CL_CD_cruise
        self.c_p = 90 * 10**-3 * 10**-6
        self.R = 1500 * 1000
        self.V = 475 * 1000 / 3600
        self.E = self.R / self.V
        self.efficiency = 0.85
        self.CL_alpha = 0
        self.CLh_alpha = 0
        self.CLw_alpha = 0
        self.Mach = self.V/np.sqrt(1.4*287*self.ISA(self.cruise_altitude)[1])
        self.w_s = self.find_DP()[0] / (9.81/self.kg_to_pounds*self.meters_to_feet**2)
        self.w_p = self.find_DP()[1] *self.kg_to_pounds / (9.81*self.watts_to_horsepower)


        #### Powertrain parameters ####
        self.delta_t_func = None
        self.delta_T = None
        self.T_air = None
        self.waste_heat_power = None

        self.n_ee = 0.9
        self.n_pmad = 0.9
        self.n_fc = 0.6
        self.n_comp = 0.7
        self.n_fuel_tank = 0.5

        self.m_comp = 0
        self.m_cooling = 0
        self.m_fuel_cell = 0
        self.m_pmad = 0
        self.m_electric_engine = 0

        self.rho_pmad = 10000 * (self.watts_to_horsepower / self.kg_to_pounds)
        self.rho_comp = 2000 * (self.watts_to_horsepower / self.kg_to_pounds)
        self.rho_ee = 2800 * (self.watts_to_horsepower / self.kg_to_pounds)
        self.rho_fc = 3300 * (self.watts_to_horsepower / self.kg_to_pounds)

        self.pmad_power = None
        self.engine_power = None
        self.comp_power = None
        self.fc_power = None
        self.fc_des_power = self.fc_power

        self.delta_T = 25
        self.T_air = 250

        self.c_p_air = 1003
        self.lamda_o2 = 1.75
        self.T_t1 = self.ISA(self.cruise_altitude)[1]*(1+self.Mach**2 * (1.4 - 1) / 2)
        self.PR = 101325 *1.05/ self.ISA(self.cruise_altitude)[0]
        self.T_t2 = self.T_t1 * (1 + (1 / self.n_comp) * ((self.PR)**((0.4 / 1.4))-1))

        ########## Geometrical parameters #############
        self.height_fus = 1.73 * self.meters_to_feet
        self.width_fus = 1.9 * self.meters_to_feet
        self.diameter_fus = 1.9 * self.meters_to_feet
        self.lh = 5.9 * self.meters_to_feet
        self.lv = 5.4 * self.meters_to_feet
        self.t_c = 0.1
        self.fuel_length = 0
        self.length_tailcone = 3.70*self.meters_to_feet

        self.fractions = 0.992 * 0.996 * 0.996 * 0.990 * 0.992 * 0.992
        self.fuel_factor = 0
        self.AR = 10
        self.sweep_angle = 4 * np.pi / 180
        self.sweep_angle_horizontal = 20 * np.pi / 180
        self.sweep_angle_vertical = 20 * np.pi / 180
        self.q = 0.5 * 1.225 * (self.V)**2 * (self.kg_to_pounds / (self.meters_to_feet**2))
        self.taper_ratio = 0.4
        self.lamda = self.taper_ratio
        self.root_chord = 2.5 *self.meters_to_feet
        self.taper_ratioh = 1
        self.taper_ratiov = 0.8
        self.mac = 1.85 * self.meters_to_feet # Assumed
        self.cockpitlength = 2.52 *self.meters_to_feet
        self.payloadlength = 5.1*self.meters_to_feet
        self.insulation_length = 2.1*self.meters_to_feet
        self.length_fus = [(self.cockpitlength+self.payloadlength+self.length_tailcone) ]

        # self.mac = self.root_chord * 2 / 3 * (1 + self.taper_ratio + self.taper_ratio ** 2) / (1 + self.taper_ratio)


        # tail volumes from https://onlinelibrary.wiley.com/doi/pdf/10.1002/9781118568101.app1

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
        self.surface_controlh = 51.09013541454193
        self.component_matrix = []
        self.fuel_diameter = 1.56*self.meters_to_feet
        #self.FC = FuelCellSizing(10)
        #self.FC.fit_plots()

    def class1(self):
        cruise_fraction = np.exp(self.R*(9.81*self.c_p)/(self.efficiency*self.L_D_cruise))
        f1 = 1/cruise_fraction
        loiter_fraction = np.exp(self.E*(9.81*self.c_p)/(self.V*self.L_D_loiter))
        f2 = 1/loiter_fraction
        if self.iter>0:
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
        # Engine power parameters
        self.shaft_power = self.w_mtow / self.w_p
        self.electric_net = self.shaft_power / self.n_ee
        self.m_electric_engine = self.electric_net / self.rho_ee

        # Parts of fuel cell power equation
        self.delta_t_func = 0.0038 * (self.T_air / self.delta_T) ** 2 + 0.0352 * (self.T_air / self.delta_T) + 0.1817
        part1 = (1 - 1/self.n_fc) * self.delta_t_func
        part2 = (self.T_t1-self.T_t2) *self.c_p_air*2.856*10**-7*self.lamda_o2/(self.n_fc*self.n_ee)
        part3 = self.electric_net + 1.33 * self.delta_t_func * self.watts_to_horsepower

        # Calculate Powers
        self.fc_power = part3/(1+0.371*part1 + part2)
        #if self.pm_it == 0:
        #    self.fc_des_power = self.fc_power
        self.cool_power = (-1 * part1 * self.fc_power * 0.371 + 1.33 * self.watts_to_horsepower) * self.delta_t_func
        self.waste_heat_power = (1 / self.n_fc - 1) * self.fc_power
        self.comp_power = -1*part2 *self.fc_power

        # Calculate powertrain component masses
        self.m_fuel_cell = self.fc_power / self.rho_fc
        self.m_cooling = (0.194 * self.waste_heat_power + 1.39 * self.watts_to_horsepower) * self.delta_t_func
        self.m_comp = self.comp_power / self.rho_comp                       # lbs <- hp / [hp/lbs]
        self.m_pmad = self.fc_power / self.rho_pmad
        self.w_installedEngine = 1.2 * (self.m_electric_engine + self.m_fuel_cell + self.m_pmad + self.m_cooling + self.m_comp)

        #mass_ratio = (self.w_fuel + self.w_fueltank) / self.m_fuel_cell
        #pmax_p = self.FC.prat(mass_ratio)
        #p_pmax = 1/pmax_p

        # print('mass ratio', mass_ratio)
        # print('power ratio', pmax_p)
        # print('FC efficiency', self.FC.nu(p_pmax))
        #
        # print(self.pm_it)

        # self.fc_des_power = self.fc_power * pmax_p
        # if (abs(self.FC.nu(p_pmax) - self.n_fc) < 0.01) and (self.pm_it < 50):
        #     self.n_fc = self.FC.nu(p_pmax)
        #
        #     print('fuel cell efficiency converged')
        # elif self.pm_it == 50:
        #     print('fuel cell efficiency did not converge')
        # else:
        #     print('FC efficiency',self.FC.nu(p_pmax))
        #     self.n_fc = self.FC.nu(p_pmax)
        #     self.pm_it += 1
        #     self.powertrain_mass()
    def reset(self):
        self.pm_it = 0
        self.kg_to_pounds = 2.20462
        self.meters_to_feet = 3.28084
        self.watts_to_horsepower = 0.00134102

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
        self.x_mlg = 0
        self.x_payload_cg = 0
        self.x_crew_cg = 0

        ######## Structure Masses ########
        self.m_wing = []
        self.m_h = 0
        self.m_v = 0
        self.m_fuselage = []
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
        self.w_battery = 50 * self.kg_to_pounds  # from https://www.aircraft-battery.com/search-by-your-aircraft/battery_detail/293
        self.w_mtow = 0
        self.w_oew = 3500 * self.kg_to_pounds
        self.w_fueltank = 200 * self.kg_to_pounds

        ########## Payload Masses ###########
        self.w_fuel = 0
        self.w_payload = 800 * self.kg_to_pounds

        ######### Performance ###########
        self.L_D_cruise = self.CL_CD_cruise
        self.L_D_loiter = self.CL_CD_cruise
        self.c_p = 90 * 10 ** -3 * 10 ** -6
        self.R = 1500 * 1000
        self.V = 475 * 1000 / 3600
        self.E = self.R / self.V
        self.efficiency = 0.85
        self.CL_alpha = 0
        self.CLh_alpha = 0
        self.CLw_alpha = 0
        self.Mach = self.V / np.sqrt(1.4 * 287 * self.ISA(self.cruise_altitude)[1])
        self.w_s = self.find_DP()[0] / (9.81 / self.kg_to_pounds * self.meters_to_feet ** 2)
        self.w_p = self.find_DP()[1] * self.kg_to_pounds / (9.81 * self.watts_to_horsepower)

        #### Powertrain parameters ####
        self.delta_t_func = None
        self.delta_T = None
        self.T_air = None
        self.waste_heat_power = None

        self.n_ee = 0.9
        self.n_pmad = 0.9
        self.n_fc = 0.6
        self.n_comp = 0.7
        self.n_fuel_tank = 0.5

        self.m_comp = 0
        self.m_cooling = 0
        self.m_fuel_cell = 0
        self.m_pmad = 0
        self.m_electric_engine = 0

        self.rho_pmad = 10000 * (self.watts_to_horsepower / self.kg_to_pounds)
        self.rho_comp = 2000 * (self.watts_to_horsepower / self.kg_to_pounds)
        self.rho_ee = 2800 * (self.watts_to_horsepower / self.kg_to_pounds)
        self.rho_fc = 4000 * (self.watts_to_horsepower / self.kg_to_pounds)

        self.pmad_power = None
        self.engine_power = None
        self.comp_power = None
        self.fc_power = None
        self.fc_des_power = self.fc_power

        self.delta_T = 25
        self.T_air = 250

        self.c_p_air = 1003
        self.lamda_o2 = 1.75
        self.T_t1 = self.ISA(self.cruise_altitude)[1] * (1 + self.Mach ** 2 * (1.4 - 1) / 2)
        self.PR = 101325 * 1.05 / self.ISA(self.cruise_altitude)[0]
        self.T_t2 = self.T_t1 * (1 + (1 / self.n_comp) * ((self.PR) ** ((0.4 / 1.4)) - 1))

        ########## Geometrical parameters #############
        self.height_fus = 1.73 * self.meters_to_feet
        self.width_fus = 1.9 * self.meters_to_feet
        self.diameter_fus = 1.9 * self.meters_to_feet
        self.lh = 5.9 * self.meters_to_feet
        self.lv = 5.4 * self.meters_to_feet
        self.t_c = 0.1
        self.fuel_length = 0
        self.length_tailcone = 3.70 * self.meters_to_feet

        self.fractions = 0.992 * 0.996 * 0.996 * 0.990 * 0.992 * 0.992
        self.fuel_factor = 0
        self.AR = 10
        self.sweep_angle = 4 * np.pi / 180
        self.sweep_angle_horizontal = 20 * np.pi / 180
        self.sweep_angle_vertical = 20 * np.pi / 180
        self.q = 0.5 * 1.225 * (self.V) ** 2 * (self.kg_to_pounds / (self.meters_to_feet ** 2))
        self.taper_ratio = 0.4
        self.lamda = self.taper_ratio
        self.root_chord = 2.5 * self.meters_to_feet
        self.taper_ratioh = 1
        self.taper_ratiov = 0.8
        self.mac = 1.85 * self.meters_to_feet  # Assumed
        self.cockpitlength = 2.52 * self.meters_to_feet
        self.payloadlength = 5.1 * self.meters_to_feet
        self.insulation_length = 2.1 * self.meters_to_feet
        self.length_fus = [(self.cockpitlength + self.payloadlength + self.length_tailcone +0.22*self.meters_to_feet)]

        # self.mac = self.root_chord * 2 / 3 * (1 + self.taper_ratio + self.taper_ratio ** 2) / (1 + self.taper_ratio)

        # tail volumes from https://onlinelibrary.wiley.com/doi/pdf/10.1002/9781118568101.app1

        ####### Class 1 Statistical Data ############
        self.MTOWstat = np.multiply(
            [14330, 16424, 46500, 22900, 25700, 12500, 15245, 11300, 12500, 8200, 9850, 14500, 36000, 8500, 45000,
             34720, 5732, 7054, 28660, 44000, 41000, 21165, 26000, 9000], 1)
        self.OEWstat = np.multiply(
            [7716, 9072, 26560, 14175, 16075, 7750, 8500, 6494, 7538, 4915, 5682, 8387, 23693, 4613, 25525, 20580, 3245,
             4299, 16094, 27000, 24635, 11945, 15510, 5018], 1)
        self.subsystem_weightage = dict()
        self.subsystem_weightage = {'fuselage': 10, 'wing': 8, 'tail': 1.3, 'undercarriage': 4.5, 'nacelle': 3,
                                    'engines': 9}
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
        self.vertical_volume = 0.03 * (self.surface_wing * self.b_w + 10 * self.height_fus ** 2 * self.length_fus[-1])
        self.horizontal_volume = 0.2 * (
                    self.surface_wing * self.mac + 2 * self.width_fus ** 2 * self.length_fus[-1]) * (self.AR + 2) / (
                                             self.AR - 2)
        self.surface_controlv = self.vertical_volume / self.lv
        self.surface_controlh = self.horizontal_volume / self.lh
        self.surface_controlh = 51.09013541454193
        self.component_matrix = []
        self.fuel_diameter = 1.56 * self.meters_to_feet

    def class2(self):

        self.w_design = self.w_oew - self.w_crew
        Ht_Hv = 1
        ###### Link for mass estimations used #######

        ###### https://www.ijemr.net/DOC/AircraftMassEstimationMethods(170-178).pdf ######
        ###### https://brightspace.tudelft.nl/d2l/le/content/419892/viewContent/2368629/View ######  <--- all raymer formulas


        self.pressurised_volume = self.diameter_fus**2*np.pi*self.length_fus[-1]/4
        self.m_fuselage.append(0.052*(self.length_fus[-1]*self.diameter_fus*np.pi)**1.086*(self.w_design*self.limit_load*self.limit_factor)**0.117*self.lh**(-0.051)*(self.CL_CD_cruise)**(-0.072)*self.q**0.241+11.9+(self.pressurised_volume*8)**0.271)
        self.m_wing.append(0.036*self.surface_wing**(0.758)*(800*2.208)**0.0035*(self.AR/(np.cos(self.sweep_angle)**2))**0.6*self.q**(0.006)*self.taper_ratio**0.04*(100*self.t_c/(np.cos(self.sweep_angle)))**-0.3*(self.limit_factor*self.limit_load*self.w_design)**0.49)

        # Horizontal stabilizer mass
        self.m_h = 0.016*(self.limit_factor*self.limit_load*self.w_design)**0.414*self.q**(0.168)*self.surface_controlh**(0.896)*\
                 (100*self.t_c/np.cos(self.sweep_angle_horizontal))**(-0.12)

        # Vertical stabilizer mass
        self.m_v = 0.073*(1+0.2*(Ht_Hv))*(1.5*2.5*self.w_design)**0.376*self.q**0.122*self.surface_controlv**(0.873)*\
                   (100*self.t_c/(np.cos(self.sweep_angle_vertical)))**(-0.49)*\
                   (self.AR/(np.cos(self.sweep_angle_vertical)**2))**(0.357)*(self.taper_ratiov)**0.039  #checked
        # Installed Engine mass
        self.pm_it = 0

        self.powertrain_mass()


        # Landing Gear Group mass
        self.m_mlg = 0.095 * (self.ult_factor * self.w_mtow) ** 0.768 * (self.length_mlg / 12) ** 0.409
        self.m_nlg = 0.125 * (self.ult_factor * self.w_mtow) ** 0.566 * (self.length_nlg / 12) ** 0.845

        # Miscellaneous subsystems
        self.w_flightcontrols = 0.053 * self.length_fus[-1]**(1.536) * self.b_w ** (0.371) * (self.limit_factor*self.limit_load*self.w_design*10e-4)**0.8
        self.w_hydraulics = 0.001 * self.w_design
        self.w_electrical = 12.57 * (self.w_fuelsystem+self.w_avionics) ** 0.51
        self.w_avionics = 2.177*800**0.933  # fine
        self.w_icing = 0.265 * self.w_design ** 0.52 * self.n_passengers**0.68 * self.w_avionics ** 0.07 * self.Mach * 0.08
        self.w_furnishing = 0.0582 * self.w_design - 65
        # print(self.w_furnishing/self.kg_to_pounds)
        # self.w_furnishing = 0

        ###### updating OEW ########
        self.w_fueltank = ((1 - self.n_fuel_tank) / self.n_fuel_tank) * self.w_fuel

        self.fuel_volume = self.w_fuel*2.8 / (71 * self.kg_to_pounds / (self.meters_to_feet ** 3))
        self.w_fuelsystem = 2.49*self.fuel_volume**0.726*(1/(1+1.1))**0.363*2**0.242*2**0.157

        self.w_oew = (self.m_fuselage[-1] + self.m_h + self.m_v + self.m_wing[-1] + self.w_furnishing +
                     self.w_icing + self.w_electrical + self.w_avionics + self.w_fuelsystem
                     + self.w_flightcontrols + self.w_installedEngine + self.w_hydraulics+self.w_fueltank+self.w_battery)

        ###### updating MTOW ########
        self.w_mtow = self.w_oew +self.w_payload + self.w_fuel

        self.iter += 1


    def oew(self):
        oew = (self.m_fuselage[-1] + self.m_h + self.m_v + self.m_wing[-1] + self.w_furnishing +
                     self.w_icing + self.w_electrical + self.w_avionics + self.w_fuelsystem
                     + self.w_flightcontrols + self.w_installedEngine + self.w_hydraulics+self.w_fueltank+self.w_battery)
        return oew

    def mtow(self):
        mtow = self.oew() + self.w_fuel + self.w_payload
        return mtow

    def print_length(self, parameter, name=''):
        print(name,'= %.2f' % (parameter / self.meters_to_feet), 'm')

    def print_mass(self, parameter, name=''):
        print(name,'= %.2f' % (parameter / self.kg_to_pounds), 'kg')

    def print_power(self, parameter, name=''):
        print(name,'= %.2f' % (parameter / (self.watts_to_horsepower * 1000)), 'kW')

    def mainsizing(self):
        self.fuel_volume = self.w_fuel / (71 * self.kg_to_pounds / (self.meters_to_feet**3))/0.9
        self.fuel_length = self.fuel_volume / ((self.fuel_diameter) **2 * np.pi / 4) +0.3*self.meters_to_feet
        self.length_fus.append(self.length_fus[0] + self.fuel_length)
        self.x_fuselage_cg = self.length_fus[-1] / 2
        self.x_fuel_cg = self.cockpitlength +self.payloadlength+ 0.5 *self.fuel_length
        # self.change = (self.length_fus[-1] / self.length_fus[0]) * self.subsystem_weightage['fuselage']/100 + (1-self.subsystem_weightage['fuselage']/100)
        # self.m_fuselage.append(self.change * self.m_fuselage[-1])
        # self.m_wing.append(self.m_wing[-1] * self.change)
        # self.surface_wing = self.w_mtow / self.w_s
        # self.w_fueltank = ((1 - self.n_fuel_tank) / self.n_fuel_tank) * self.w_fuel
        # self.w_oew = self.oew()
        # self.w_mtow = self.mtow()
        pass

    def classiter(self):
        self.class1()
        OEW1 = self.w_oew
        self.class2()
        OEW2 = self.w_oew
        mass_vec = np.array([self.m_fuselage[-1], self.m_h, self.m_v, self.m_wing[-1], self.w_furnishing, self.w_icing,
            self.w_electrical, self.w_avionics, self.w_fuelsystem, self.w_flightcontrols, self.w_installedEngine, self.w_hydraulics])
        self.component_matrix.append(mass_vec)

        if np.abs(OEW2 - OEW1)/OEW2 >= 0.01:
            self.classiter()



    def printing(self):

        #self.print_length(self.diameter_fus,'fuse diam')
        #self.print('design weight',self.w_design / self.kg_to_pounds )
        #self.print_length(self.lh, 'lh')
        #print('cl/cd cruise',self.CL_CD_cruise)
        #self.print('dyn pressure',self.q / (self.kg_to_pounds * self.meters_to_feet))
        #self.print('pressurized volume',self.pressurised_volume * 0.3048 ** 3)
        #self.print_mass(self.w_fuelsystem, 'fuel system mass')
        #self.print('--------')
        #print('Power loading = ', self.w_p * 9.81 / self.kg_to_pounds * self.watts_to_horsepower, 'N/W')

        print('\nGeneral Aircraft Parameters:\n--------------')
        self.print_length(self.length_fus[-1],'fuselage length ')
        self.print_mass(self.m_fuselage[-1],'fuselage mass ')
        self.print_mass(self.w_mtow , 'MTOW')
        self.print_mass(self.w_oew, 'OEW')
        print('Wing Area = %.2f' % (self.surface_wing/(3.28**2)), 'm^2')
        self.print_length(self.b_w, 'Wingspan')

        print('\nPower Values:\n---------------')
        self.print_power(self.shaft_power , 'Shaft power')
        self.print_power(self.comp_power, 'Compressor power')
        self.print_power(self.fc_power, 'Fuel cell power')
        self.print_power(self.cool_power, 'cooling power')

        print('Compressor power = ', self.comp_power/self.watts_to_horsepower/1000)
        print('FC power = ', self.fc_power/self.watts_to_horsepower/1000)
        print('cooling power:', self.cool_power/self.watts_to_horsepower/1000)
        # print('cooling system mass:')
        # self.print_mass(self.m_cooling)
        # print('compressor mass:')
        # self.print_mass(self.m_comp)
        # print('fuel cell mass:')
        # self.print_mass(self.m_fuel_cell)
        # print('electric engine mass:')
        # self.print_mass(self.m_electric_engine)
        # print('Pressure ratio ', self.PR)
        # print('----------------')
        print('\nPowertrain Mass Values:\n--------------')
        self.print_mass(self.m_cooling, 'Cooling system mass')
        self.print_mass(self.m_comp, 'Compressor mass')
        self.print_mass(self.m_fuel_cell, 'Fuel cell mass')
        self.print_mass(self.m_electric_engine, 'Electric engine mass')
        self.print_mass(self.w_fuel, 'Fuel mass')
        self.print_mass(self.w_fueltank, 'Tank mass')
        self.print_length(self.fuel_length, 'Fuel tank length')

        self.print_length(self.fuel_volume/(self.meters_to_feet**2), 'Volume m^3')
        print(self.fuel_volume*71/(self.meters_to_feet**3))

        print('fuel cell efficiency', self.n_fc)

        #print('Pressure ratio ', self.PR)
        #print('----------------')


    def plot_mass_progression(self):
        labels = ['fuselage', 'horizontal stab', 'vertical stab', 'wing', 'furnishing', ' de-icing', ' electronics', 'avionics', ' fuelsystem', ' flightcontrols',  'engine', ' hydraulics']
        self.component_matrix = np.array(self.component_matrix).transpose()

        for i in range(1,13):
            x = range(self.iter)
            y = self.component_matrix[i-1]
            plt.figure()
            plt.plot(x, y, label=labels[i-1])
            plt.legend()
            plt.show()

    def cgcalc(self):
        self.tip_chord = self.root_chord*self.taper_ratio
        # self.x_wing_cg = ((1.25)*(self.root_chord*self.b_w/2)-(2)*((self.root_chord-self.taper_ratio*self.root_chord)*self.b_w/2*0.5))/(((self.root_chord-self.taper_ratio*self.root_chord)*self.b_w*0.5)+(self.root_chord*self.b_w/2))
        self.x_wing_cg = ((self.tip_chord**2*0.5*self.b_w)+((self.root_chord-self.tip_chord)*0.5*self.b_w)*(self.tip_chord+(2/3)*(self.root_chord-self.tip_chord)))/(self.b_w*self.tip_chord+(self.root_chord-self.tip_chord)*self.b_w*0.5)/self.root_chord
        self.y_mac = ((self.tip_chord*self.b_w*0.5)+((self.root_chord-self.tip_chord)*self.b_w*0.5)*(1/3))/(((self.root_chord-self.tip_chord)*self.b_w*0.5)+self.tip_chord*self.b_w)

    def cg_lists(self):
        weights = {"fuselage": self.m_fuselage[-1], "empennage": self.m_h + self.m_v, "mlg": self.m_mlg, "nlg": self.m_nlg, "crew": self.w_crew, "wing": self.m_wing[-1], "battery": self.w_battery, "engine": self.w_installedEngine, "fueltank": self.w_fueltank, "mtow": self.w_mtow, "oew": self.w_oew, "payload": self.w_payload, "fuel": self.w_fuel}
        fuselage_cg = {"fuselage": self.x_fuselage_cg, "empennage": self.x_empennage_cg, "mlg": self.x_landingGear_cg, "nlg": self.x_nlg_cg, "crew": self.x_fuselage_cg, "fueltank": self.x_fuel_cg, "payload": self.x_payload_cg, "fuel": self.x_fuel_cg}
        wing_cg = {"wing": self.x_wing_cg, "battery": self.x_battery, "engine": self.x_engine_cg}
        mac = self.mac
        return weights, fuselage_cg, wing_cg, mac

    def landinggearsizing(self):

        pass

    def empennagesizing(self):


        pass

    def classiter2(self):
        self.class1()
        OEW1 = self.w_oew
        self.class2()
        OEW2 = self.w_oew
        self.mainsizing()
        mass_vec = np.array([self.m_fuselage[-1], self.m_h, self.m_v, self.m_wing[-1], self.w_furnishing, self.w_icing,
            self.w_electrical, self.w_avionics, self.w_fuelsystem, self.w_flightcontrols, self.w_installedEngine, self.w_hydraulics])
        self.component_matrix.append(mass_vec)
        if np.abs(OEW2 - OEW1)/OEW2 >= 0.01:
            self.classiter2()
            # self.mainsizing()

    def mainprocedures(self):
        self.classiter2()
        self.cgcalc()

if __name__ == "__main__":
    aircraft = Aircraft()
    aircraft.mainprocedures()
    aircraft.printing()