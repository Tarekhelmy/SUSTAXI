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


class OperatorBusiness:

    def __init__(self):

        # Revenue constants
        self.flighthour_rate = 2350             # USD
        self.average_flighttime = 2             # hrs RESEARCH THIS
        self.flights_per_day = 3                # RESEARCH THIS

        # Cost constants [USD]
        self.average_payload = 3                # pax, RESEARCH THIS
        self.trip_fuel_cost = None              # USD
        self.trip_staff_cost = 300 * 2 * 2      # USD/hr * hr * pilots
        self.monthly_interest = None            # RESEARCH THIS
        self.monthly_devaluation = None          # RESEARCH THIS
        self.
