import matplotlib.pyplot as plt
import numpy as np
#from Aircraft_simulation.mass_estimations import Aircraft
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

"""


class OperatorBusiness(Stability):

    def __init__(self):

        super().__init__()
        self.procedures()

        # Miscellaneous constants
        self.mission_range = 1000*1000                               # m
        self.flights_per_day = 3                                     # RESEARCH THIS
        self.average_flighttime = 2                                  # hrs RESEARCH THIS
        self.fleet_size = 10
        self.unit_price = 4.25 * 1e6                                 # USD

        # Revenue constants
        self.flighthour_rate = 2350                                  # USD

        # Cost constants
        self.average_payload = 3                                     # pax, RESEARCH THIS
        self.hydrogen_cost = 7                                       # USD/kg RESEARCH THIS
        self.trip_fuel_cost = None                                   # USD RESEARCH THIS
        self.hourly_staff_cost = 200                                 # USD/hr/pilot RESEARCH THIS
        self.interest_rate = 0.00407412378                           # (%/100)/month RESEARCH THIS
        self.monthly_devaluation = self.unit_price / (20*12)         # USD/month RESEARCH THIS
        self.overhead = 1e5                                          # USD/month RESEARCH THIS (includes: office, marketing, ground staff & storage)
        self.airport_fees = 300                                      # USD per flight RESEARCH THIS
        self.maintenance = 300                                       # USD per flighthour RESEARCH THIS

        self.balance = -1 * self.fleet_size * self.unit_price * 1.1  # 1.1 = factor for miscellaneous initial investment

    def plot_profit(self, runtime):

        # Calculate monthly revenue
        flight_revenue = self.flighthour_rate * self.average_flighttime
        monthly_revenue = flight_revenue * self.flights_per_day * self.fleet_size * (365/12)

        # Calculate monthly cost
        self.trip_fuel_cost = self.find_fuel() * self.hydrogen_cost
        trip_cost = 0
        trip_cost += self.trip_fuel_cost
        trip_cost += (2 * self.hourly_staff_cost + self.maintenance) * self.average_flighttime
        trip_cost += self.airport_fees

        monthly_cost = 0
        monthly_cost += trip_cost * self.flights_per_day * self.fleet_size * (365/12)
        monthly_cost += self.overhead + self.monthly_devaluation * self.fleet_size

        # Calculate the balance over time for the operator
        monthly_profit = monthly_revenue - monthly_cost
        balance_over_time = np.zeros((runtime, 2))
        balance_over_time[:, 0] = range(1, runtime + 1)

        print(balance_over_time)
        for month in balance_over_time[:, 0]:
            month = int(month-1)
            self.balance += monthly_profit
            if self.balance < 0:
                self.balance *= (1+self.interest_rate)
            balance_over_time[month, 1] = self.balance

        # Plot operator balance over time
        fix, ax = plt.subplots()
        ax.plot(balance_over_time[:, 0], balance_over_time[:, 1])
        ax.set_title("Operator balance over time")
        ax.set_xlabel("Month number")
        ax.set_ylabel("Balance [USD]")
        plt.show()

    def find_fuel(self):

        # Recalculate the fuel fraction for average mission
        mission_fraction = np.exp(self.mission_range * (9.81 * self.c_p) / (self.efficiency * self.L_D_cruise))
        self.fuel_factor = 1 - ((1 / mission_fraction) * self.fractions)
        ff = self.fuel_factor * (40/120)

        # Recalculate MTOW and fuel burn for average mission
        self.w_mtow -= (6 - self.average_payload) * (800/6)
        fuel_burn = self.w_mtow * ff * (1 / self.kg_to_pounds)
        print(fuel_burn)
        return fuel_burn

if __name__ == "__main__":

    Company = OperatorBusiness()
    Company.plot_profit(120)



