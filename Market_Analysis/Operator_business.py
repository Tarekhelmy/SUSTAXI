import matplotlib.pyplot as plt
import numpy as np
from Aircraft_simulation.mass_estimations import Aircraft

from Aircraft_simulation.barchart import BarChart
from Aircraft_simulation.Stability import Stability

"""
The business model of the manufacturer
---------------
--- Revenue ---
---------------
- Average paying customer
- hourly cost
- Average flights / day / operator

------------
--- Cost ---
------------
- Average fuel cost per trip (consider average payload)
- Initial investment interest
- Devaluation of assets
- office overhead
- marketing costs
- staff salary
- maintenance
- airport fees

RESEARCH
31% CAPEX increase
47% maintenance increase (assuming hydrogen combustion)
7% less flight cycles due to longer refueling times (not applicable here?)
Airport and ATC cost --> no change



"""


class OperatorBusiness(Stability):

    def __init__(self):

        super().__init__()
        self.procedures()

        # Miscellaneous constants
        self.mission_range = 1000*1000                               # m
        self.flights_per_day = 3                                     # RESEARCH THIS (Estimated)
        self.average_flighttime = 2                                  # hrs RESEARCH THIS (Estimated, based on range)
        self.fleet_size = 325                                        # 25% of the 4*983 flights per day with 3 flights per day
        self.unit_price = 6.5 * 1e6                                  # USD
        self.breakevenpoint = 10
        # Revenue constants

        self.flighthour_rate = 2350                                 # USD
        self.ratechange = 0

        # Cost constants
        self.average_payload = 3                                     # pax, RESEARCH THIS --> half loading https://www.globeair.com/b/private-jet-travellers-statistics
        self.hydrogen_cost = 7                                       # USD/kg RESEARCH THIS
        self.trip_fuel_cost = None                                   # USD RESEARCH THIS
        self.monthly_staff_cost = 5000                               # USD/month/pilot RESEARCH THIS
        self.interest_rate = 0.00407412378                           # (%/100)/month RESEARCH THIS
        self.monthly_devaluation = 0        # USD/month RESEARCH THIS
        self.overhead = 0.1081                                          # USD/month percentage RESEARCH THIS (includes: office, marketing, ground staff & storage)
        self.airport_fees = 0.2648                                      # USD per flight  percentage RESEARCH THIS
        self.maintenance = 0.1160                                      # USD per flighthour  percentage RESEARCH THIS
        self.balance = -1 * self.fleet_size * self.unit_price * 1.1  # 1.1 = factor for miscellaneous initial investment
        self.divfactor = self.maintenance +self.overhead+ self.airport_fees


    def plot_profit(self, runtime):

        # Calculate monthly revenue
        flight_revenue = self.flighthour_rate * self.average_flighttime
        monthly_revenue = flight_revenue * self.flights_per_day * self.fleet_size * (365/12)

        # Calculate monthly cost
        self.trip_fuel_cost = self.find_fuel() * self.hydrogen_cost
        trip_cost = 0
        trip_cost += self.trip_fuel_cost
        trip_cost +=  0
        trip_cost += 0


        monthly_cost = self.monthly_staff_cost*2*self.fleet_size
        monthly_cost += trip_cost * self.flights_per_day * self.fleet_size * (365/12)
        monthly_cost += 0 + self.monthly_devaluation * self.fleet_size
        monthly_cost /=(1-self.divfactor)
        self.overhead = 0.1081*monthly_cost
        self.airport_fees = 0.2648*monthly_cost /(self.flights_per_day * self.fleet_size * (365/12))
        self.maintenance = 0.1160*monthly_cost/(self.flights_per_day * self.fleet_size * (365/12)* self.average_flighttime)
        # Calculate the balance over time for the operator
        monthly_profit = monthly_revenue - monthly_cost
        plt.pie([self.trip_fuel_cost* self.flights_per_day * self.fleet_size * (365/12)*100/monthly_cost,self.monthly_staff_cost*2* self.fleet_size*100/monthly_cost,
                 self.overhead*100/monthly_cost,self.airport_fees*self.flights_per_day * self.fleet_size * 100*(365/12)/monthly_cost,
                 self.maintenance*100*self.flights_per_day * self.fleet_size * (365/12)* self.average_flighttime/monthly_cost,self.interest_rate*100],
                explode=(0.1,0.1,0.1,0.1,0.1,0.1),labels = ['Fuel','Crew cost','Airport fees','Overhead','Maintenance','Interest'],autopct='%1.1f%%',
         startangle=90)
        plt.show()

        print('total flights per month is = ', self.flights_per_day * self.fleet_size * (365/12))
        balance_over_time = np.zeros((runtime, 2))
        balance_over_time[:, 0] = range(1, runtime + 1)
        for month in balance_over_time[:, 0]:
            month = int(month-1)
            self.balance += monthly_profit
            if self.balance < 0:
                self.balance *= (1+self.interest_rate)
            balance_over_time[month, 1] = self.balance
        # Plot operator balance over time
        fix, ax = plt.subplots()
        ax.plot(balance_over_time[:, 0], balance_over_time[:, 1])
        ax.set_title("Operator profit over time")
        ax.set_xlabel("Month number")
        ax.set_ylabel("Profit [USD]")
        plt.show()


    def find_fuel(self):

        # Recalculate the fuel fraction for average mission
        mission_fraction = np.exp(self.mission_range * (9.81 * self.c_p) / (self.efficiency * self.L_D_cruise))
        self.fuel_factor = 1 - ((1 / mission_fraction) * self.fractions)
        ff = self.fuel_factor * (40/120)
        # Recalculate MTOW and fuel burn for average mission
        self.w_mtow -= (6 - self.average_payload) * (800/6)
        fuel_burn = self.w_mtow * ff * (1 / self.kg_to_pounds)
        return fuel_burn

    def breakeven(self):
        self.flighthour_rate+=self.ratechange



        pass

if __name__ == "__main__":

    Company = OperatorBusiness()
    Company.plot_profit(120)



