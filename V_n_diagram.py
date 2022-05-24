from lib2to3.pgen2.token import VBAR
import numpy as np
import matplotlib.pyplot as plt

from Wing_Power_Loading import WingAndPowerSizing

class VNDiagram(WingAndPowerSizing):

    def __init__(self, MTOW):
        super().__init__(MTOW)
        self.loadfactor = 2.1 + 24000 / (self.MTOW * 0.2248 + 10000)
        #From CS-23
        self.mac = 1.85
        self.Mach = self.cruise_speed / (np.sqrt(1.4 * 287 * self.ISA(self.cruise_altitude)[1]))
        self.density = super().ISA(self.cruise_altitude)[2]
        self.W_S = super().find_DP()[0]
        self.negloadfactor = -0.4 * self.loadfactor
        #From CS-23
        
        self.CLcurve = (2 * np.pi * self.AR * 1.2) / (2 + np.sqrt(4 + (self.AR * 1.2 * np.sqrt(1 - self.Mach ** 2 ) / 0.95) ** 2 * (1 + 1 / (1 - self.Mach ** 2))))
        #DATCOM method

        self.mu = (2 * self.W_S) / (self.density * 32.2 * self.mac * self.CLcurve)
        self.alleviationfactor = 0.88 * self.mu / (5.3 + self.mu)
    
    def V_n_diag(self):
        
        VA = np.sqrt((self.loadfactor * self.W_S) / (0.5 * self.density * self.CLmax_clean))
        loading = [0.5 * self.density * V ** 2 * self.CLmax_clean / self.W_S for V in np.linspace(0, VA, 500)]

        VC = self.cruise_speed

        VD = 1.25 * VC
        #Taken from CS-23

        VS = np.sqrt((-self.negloadfactor * self.W_S) / (0.5 * self.density * self.CLmax_clean))
        #This occurs at load factor of 1

        negativeloading = [-0.5 * self.density * V ** 2 * self.CLmax_clean / self.W_S for V in np.linspace(0, VS, 500)]
        #Negative curve is the same as the one before but with its sign changed

        Vstall = np.sqrt((1 * self.W_S) / (0.5 * self.density * self.CLmax_clean))

        uB = self.alleviationfactor * 66 / 3.28084
        uC = self.alleviationfactor * 50 / 3.28084
        uD = self.alleviationfactor * 25 / 3.28084

        delta_n_C = self.density * VC * self.CLcurve * uC / (2 * self.W_S)
        delta_n_D = self.density * VD * self.CLcurve * uD / (2 * self.W_S)

        n_peak_C = 1 + delta_n_C
        n_peak_D = 1 + delta_n_D

        n_neg_C = 1 - delta_n_C
        n_neg_D = 1 - delta_n_D

        VB = Vstall * np.sqrt(n_peak_C)
        #From CS-23

        delta_n_B = self.density * VB * self.CLcurve * uB / (2 * self.W_S)
        n_peak_B = 1 + delta_n_B
        n_neg_B = 1 - delta_n_B

        self.gustloadfactor = max(n_peak_B, n_peak_C, n_neg_D)
        
        plt.figure(1)
        plt.grid()
        plt.title("V-n Diagram")

        ######## MANUEVER DIAGRAM #########


        #Positive side 
        plt.plot(np.linspace(0, VA, 500), loading, linestyle="-", color="black", label="Stall curve")
        plt.plot([VA, VD], [self.loadfactor, self.loadfactor], linestyle="-", color="black", label="Dive speed")
        plt.vlines(VD, 0, self.loadfactor, linestyle="-", color="black")

        #Negative side
        plt.plot(np.linspace(0, VS, 500), negativeloading, linestyle="-", color="black", label="Negative load factor curve")
        plt.plot([VS, VC], [self.negloadfactor, self.negloadfactor], linestyle="-", color="black", label="Design Cruise speed")
        plt.plot([VC, VD], [self.negloadfactor, 0], linestyle="-", color="black")

        #Stall speed line
        plt.hlines(1, 0, VD, linestyle="--", color="black", label="Stall speed line")

        ######## GUST LOADING DIAGRAM ########


        #Upper side dashed
        plt.plot([0, VB], [1, n_peak_B], linestyle="-", color="blue", label="Maximum gust intensity load factor")
        plt.plot([0, VC], [1, n_peak_C], linestyle="--", color="blue", label="Design cruise speed load factor")
        plt.plot([0, VD], [1, n_peak_D], linestyle="--", color="blue", label="Dive speed load factor")
        
        #Upper side full
        plt.plot([VB, VC], [n_peak_B, n_peak_C], linestyle="-", color="blue")
        plt.plot([VC, VD], [n_peak_C, n_peak_D], linestyle="-", color="blue")

        #Lower side dashed
        plt.plot([0, VB], [1, n_neg_B], linestyle="-", color="blue", label="Negative maximum gust intensity load factor")
        plt.plot([0, VC], [1, n_neg_C], linestyle="--", color="blue", label="Design cruise speed negative load factor")
        plt.plot([0, VD], [1, n_neg_D], linestyle="--", color="blue", label="Dive speed negative load factor")

        #Lower side full
        plt.plot([VB, VC], [n_neg_B, n_neg_C], linestyle="-", color="blue")
        plt.plot([VC, VD], [n_neg_C, n_neg_D], linestyle="-", color="blue")

        # plt.legend(loc="lower left", fontsize="small")
        plt.show()
        plt.close(1)


    def get_critical_loadfactor(self):
        print(f"The most critical load factor is: {max(self.loadfactor, self.gustloadfactor)}")
        return max(self.loadfactor, self.gustloadfactor)

        
diagram = VNDiagram(5500 * 9.81)
diagram.V_n_diag()

            