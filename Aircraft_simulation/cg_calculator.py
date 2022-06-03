import matplotlib.pyplot as plt
from mass_estimations import Aircraft


# aircraft = Aircraft()
# weights, fus_cg_locations, wing_cg_locations, mac = aircraft.cg_lists()

class CenterOfGravity(Aircraft):
    def __init__(self):
        super().__init__()
        self.classiter()
        self.mainsizing()
        self.cgcalc()
        self.updatecg()
        self.weight = self.cg_lists()
        self.weights = self.weight[0]
        self.fus_cg_locations = self.weight[1]
        self.wing_cg_locations = self.weight[2]
        self.massfractions = dict()
        self.locations = dict()
        self.lemac =  25 # ft
        self.mac = self.weight[3]
        # self.positions = self.cgandplot(False)

    def updatecg(self):
        # all positions are (x_cg - lemac) / mac
        self.x_engine_cg = 0
        self.x_battery = 0.45
        self.x_empennage_cg = 0.9 * self.length_fus[-1]  # - lemac / mac
        self.x_cargopayload = 0.9 * self.length_fus[-1]
        self.x_payload_cg = (((self.payloadlength * 0.5 + self.cockpitlength) * (self.w_payload - 200 * self.kg_to_pounds) + (
            self.x_cargopayload) * 200) / self.w_payload)
        self.x_crew = 2 / 5 * self.cockpitlength

    def script(self):
        self.updatecg()
        self.weight = self.cg_lists()
        self.weights = self.weight[0]
        self.fus_cg_locations = self.weight[1]
        self.wing_cg_locations = self.weight[2]
        self.mac = self.weight[3]
        self.massfraction()
        self.lemac_oew_pl_fuel()

    def massfraction(self):
        for entry in self.weights:
            self.massfractions[entry] = self.weights[entry] / self.weights["mtow"]
        pass

    def macpercent(self, cg):
        return (cg - self.locations["lemac"]) / self.mac

    def reverse_macpercent(self, maccg):
        return maccg * self.mac + self.locations["lemac"]

    def lemac_oew_pl_fuel(self):
        fus_masses = ["fuselage", "empennage", "crew", "fueltank"]
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
        x_wcg = self.mac * product_wcg / mass_wcg + self.lemac

        self.oew_cg_mac = (((mass_fcg * x_fcg + mass_wcg * x_wcg) / ((mass_fcg + mass_wcg))) - self.lemac) / self.mac
        # x_lemac = x_fcg + self.mac * ( (x_wcg / self.mac) * (mass_wcg / mass_fcg) - self.oew_cg_mac * (1 + mass_wcg / mass_fcg))
        x_oew = self.lemac + self.oew_cg_mac * self.mac
        # self.x_oew = x_oew
        self.locations["lemac"] = self.lemac
        self.locations["oew"] = x_oew
        self.locations["payload"] = self.fus_cg_locations["payload"]
        self.locations["fuel"] = self.fus_cg_locations["fuel"]

    # before calling this, call script
    def cgandplot(self, plot=False):
        # print(self.x_payload_cg/self.meters_to_feet)
        # print(self.locations['lemac']/self.meters_to_feet)
        # print(self.length_fus[-1]/self.meters_to_feet)
        cg_OEW = self.locations["oew"]
        cg_OEWpl = (self.massfractions["payload"] * self.locations["payload"] + self.massfractions["oew"] *
                    self.locations["oew"]) / (self.massfractions["oew"] + self.massfractions["payload"])
        cg_OEWfpl = (self.massfractions["payload"] * self.locations["payload"] + self.massfractions["oew"] *
                     self.locations["oew"] + self.massfractions["fuel"] * self.locations["fuel"]) / (
                                self.massfractions["fuel"] + self.massfractions["payload"] + self.massfractions["oew"])
        cg_OEWf = (self.massfractions["oew"] * self.locations["oew"] + self.massfractions["fuel"] * self.locations[
            "fuel"]) / (self.massfractions["fuel"] + self.massfractions["oew"])

        if plot:
            plt.figure(1)
            plt.grid()
            plt.title("Class 1 Loading Diagram")

            #Adding the cg points
            plt.plot(self.macpercent(cg_OEW), self.massfractions["oew"], marker="o", color="red", markersize=10,
                     label="OEW cg location")
            plt.plot(self.macpercent(cg_OEWpl), self.massfractions["oew"] + self.massfractions["payload"], marker="o",
                     markersize=10, color="blue", label="OEW + payload cg location")
            plt.plot(self.macpercent(cg_OEWfpl),
                     self.massfractions["oew"] + self.massfractions["payload"] + self.massfractions["fuel"],
                     markersize=10, color="green", marker="o", label="OEW + payload + fuel cg location")
            plt.plot(self.macpercent(cg_OEWf), self.massfractions["oew"] + self.massfractions["fuel"], marker="o",
                     markersize=10, color="orange", label="OEW + fuel cg location")

            #Adding lines between the points
            plt.plot([self.macpercent(cg_OEW), self.macpercent(cg_OEWpl)], [self.massfractions["oew"], self.massfractions["oew"] + self.massfractions["payload"]], linestyle="-", color="black")
            plt.plot([self.macpercent(cg_OEWpl), self.macpercent(cg_OEWfpl)], [self.massfractions["oew"] + self.massfractions["payload"], self.massfractions["oew"] + self.massfractions["payload"] + self.massfractions["fuel"]], linestyle="-", color="black")
            plt.plot([self.macpercent(cg_OEWfpl), self.macpercent(cg_OEWf)], [self.massfractions["oew"] + self.massfractions["payload"] + self.massfractions["fuel"], self.massfractions["oew"] + self.massfractions["fuel"]], linestyle="-", color="black")
            plt.plot([self.macpercent(cg_OEWf), self.macpercent(cg_OEW)], [self.massfractions["oew"] + self.massfractions["fuel"], self.massfractions["oew"]], linestyle="-", color="black")

            plt.xlabel("Percentage of MAC [%]")
            plt.ylabel("Mass fraction [-]")
            plt.legend(loc="best", fontsize="small")

            plt.savefig("cg")
            plt.close(1)

        return cg_OEW / self.meters_to_feet, cg_OEWpl / self.meters_to_feet, cg_OEWfpl / self.meters_to_feet, cg_OEWf / self.meters_to_feet

    def potato_plot(self):
        pass


if __name__ == "__main__":
    cg = CenterOfGravity()
    cg.script()
    positions = cg.cgandplot(True)
    print(f"The most forward center of gravity is at: {min(positions)} m")
    print(f"The most aft center of gravity location is at: {max(positions)} m")