import numpy as np
import matplotlib.pyplot as plt
from Estimations import Aircraft

# aircraft = Aircraft()
# weights, fus_cg_locations, wing_cg_locations, mac = aircraft.cg_lists()

class CenterOfGravity(Aircraft):
    def __init__(self):
        super().__init__()
        self.weights = self.cg_lists()[0]
        self.fus_cg_locations = self.cg_lists()[1]
        self.wing_cg_locations = self.cg_lists()[2]
        self.massfractions = dict()
        self.locations = dict()
        self.bitchassfraction = 0.25
        self.mac = self.cg_lists()[3]

    def massfraction(self):
        for entry in self.weights:
            self.massfractions[entry] = self.weights[entry] / self.weights["mtow"]
        pass

    def macpercent(self, cg):
        return (cg - self.locations["lemac"]) / self.mac
    
    def reverse_macpercent(self, maccg):
        return maccg * self.mac + self.locations["lemac"]

    def lemac_oew_pl_fuel(self):
        fus_masses = ["fuselage", "empennage", "mlg", "nlg", "crew", "fuelsystem"]
        wing_masses = ["wing", "battery", "engine"]
        mass_fcg, product_fcg = 0, 0
        mass_wcg, product_wcg = 0, 0

        for name in fus_masses:
            mass_fcg += self.weights[name]
            product_fcg += self.weights[name] * self.fus_cg_locations[name]
        
        for name in wing_masses:
            mass_wcg += self.weights[name]
            product_wcg += self.weights[name] * self.wing_cg_locations[name]

        x_fcg = product_fcg / mass_fcg
        x_wcg = self.mac * product_wcg / mass_wcg

        x_lemac = x_fcg + self.mac * ( (x_wcg / self.mac) * (mass_wcg / mass_fcg) - self.bitchassfraction * (1 + mass_wcg / mass_fcg))
        x_oew = x_lemac + self.bitchassfraction * self.mac

        self.locations["lemac"] = x_lemac
        self.locations["oew"] = x_oew
        self.locations["payload"] = self.fus_cg_locations["payload"]
        self.locations["fuel"] = self.fus_cg_locations["fuel"]


    def cgandplot(self, plot=False):
        self.massfraction()
        self.lemac_oew_pl_fuel()

        cg_OEW = self.locations["oew"]
        cg_OEWpl = (self.massfractions["payload"] * self.locations["payload"] + self.massfractions["oew"] * self.locations["oew"]) / (self.massfractions["oew"] + self.massfractions["payload"])
        cg_OEWfpl = (self.massfractions["payload"] * self.locations["payload"] + self.massfractions["oew"] * self.locations["oew"] + self.massfractions["fuel"] * self.locations["fuel"]) / (self.massfractions["fuel"] + self.massfractions["payload"] + self.massfractions["oew"])
        cg_OEWf = (self.massfractions["oew"] * self.locations["oew"] + self.massfractions["fuel"] * self.locations["fuel"]) / (self.massfractions["fuel"] + self.massfractions["oew"])

        if plot:

            plt.figure(1)
            plt.grid()
            plt.title("Class 1 Loading Diagram")

            plt.plot(self.macpercent(cg_OEW), self.massfractions["oew"], marker="o", color="blue", label="OEW cg location")
            plt.plot(self.macpercent(cg_OEWpl), self.massfractions["oew"] + self.massfractions["payload"], marker="o", color="blue", label="OEW + payload cg location")
            plt.plot(self.macpercent(cg_OEWfpl), self.massfractions["oew"] + self.massfractions["payload"] + self.massfractions["fuel"], color="blue", marker="o", label="OEW + payload + fuel cg location")
            plt.plot(self.macpercent(cg_OEWf), self.massfractions["oew"] + self.massfractions["fuel"], marker="o", color="blue", label="OEW + fuel cg location")

            plt.ylim(0, 1.2)
            plt.xlim(-0.1, 1.1)
            plt.xlabel("Percentage of MAC [%]")
            plt.ylabel("Mass fraction [-]")
            plt.legend(loc="upper right", fontsize="small")

            plt.show()
            plt.close(1)

        return cg_OEW, cg_OEWpl, cg_OEWfpl, cg_OEWf
        
    def fwd_aft(self):
        return min(self.cgandplot(False)), max(self.cgandplot(False))

    def potato_plot(self):
        pass


if __name__ == "__main__":
    cg = CenterOfGravity()
    cg.cgandplot(True)
    print(f"The most forward center of gravity is at: {cg.fwd_aft()[0]} m")
    print(f"The most aft center of gravity location is at: {cg.fwd_aft()[1]} m")
