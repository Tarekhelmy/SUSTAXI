import matplotlib.pyplot as plt
import numpy as np

# These are the gCO2-eq/kWh for different electricity
Wind_onshore_GWP_p_kWh = 12.4
Wind_offshore_GWP_p_kWh = 14.2
Wind_mix_GWP_p_kWh = (Wind_onshore_GWP_p_kWh + Wind_offshore_GWP_p_kWh)/2
Hydro_near_GWP_p_kWh = 5.6
Solar_ground_GWP_p_kWh = 11.4
Other_Renewables_GWP_p_kWh = (Wind_mix_GWP_p_kWh + Hydro_near_GWP_p_kWh + Solar_ground_GWP_p_kWh)/3
Biopower_GWP_p_kWh = 64
Nuclear_PWR_GWP_p_kWh = 4.7
Coal_GWP_p_kWh = 930
Coal_cc_GWP_p_kWh = 200
Gas_GWP_p_kWh = 530
Gas_cc_GWP_p_kWh = 250
Oil_GWP_p_kWh = 951
Oil_cc_GWP_p_kWh = Coal_cc_GWP_p_kWh/Coal_GWP_p_kWh*Oil_GWP_p_kWh

# European Electricity mix 2019
Oil_TWh = 53.6
Gas_TWh = 774.2
Coal_TWh = 689.5
Nuclear_TWh = 930
Hydro_TWh = 627.9
Wind_TWh = 460
Solar_TWh = 152.8
Other_Renewables_TWh = 227.2
tot_TWh_2019 = Oil_TWh + Gas_TWh + Coal_TWh + Nuclear_TWh + Hydro_TWh +\
          Wind_TWh + Solar_TWh + Other_Renewables_TWh
# Other_TWh = 76.9

# Prognosis 2030 percent
Solar_2030 = 7
Wind_2030 = 18
Hydro_2030 = 11
Biopower_2030 = 8
Gas_2030 = 19
Oil_2030 = 0
Coal_2030 = 15
Nuclear_2030 = 22

# Prognosis 2050 percent
Solar_2050 = 11
Wind_2050 = 25
Hydro_2050 = 11
Biopower_2050 = 9
Gas_2050 = 21
Oil_2050 = 0
Coal_2050 = 5
Nuclear_2050 = 18

# Without Hydrocarbons
Solar_wo_HC = 33
Wind_wo_HC = 50
Hydro_wo_HC = 11
Biopower_wo_HC = 0
Gas_wo_HC = 6
Oil_wo_HC = 0
Coal_wo_HC = 0
Nuclear_wo_HC = 0

# ---
Shares_Euro_2019 = np.array([Oil_TWh, Gas_TWh, Coal_TWh, Nuclear_TWh, Hydro_TWh,
                  Wind_TWh, Solar_TWh, Other_Renewables_TWh])/tot_TWh_2019

Euro_mix_GWP_p_kWh = np.array([Oil_GWP_p_kWh, Gas_GWP_p_kWh, Coal_GWP_p_kWh, Nuclear_PWR_GWP_p_kWh, Hydro_near_GWP_p_kWh,
                               Wind_offshore_GWP_p_kWh, Solar_ground_GWP_p_kWh, Other_Renewables_GWP_p_kWh])

Euro_mix_with_CC_GWP_p_kWh = np.array([Oil_cc_GWP_p_kWh, Gas_cc_GWP_p_kWh, Coal_cc_GWP_p_kWh, Nuclear_PWR_GWP_p_kWh, Hydro_near_GWP_p_kWh,
                                       Wind_offshore_GWP_p_kWh, Solar_ground_GWP_p_kWh, Other_Renewables_GWP_p_kWh])

Shares_Prognostic_2030 = np.array([Solar_2030, Wind_2030, Hydro_2030, Biopower_2030, Gas_2030, Oil_2030, Coal_2030, Nuclear_2030])/100

Prognostic_2030_GWP_p_kWh = np.array([Solar_ground_GWP_p_kWh, Wind_onshore_GWP_p_kWh, Hydro_near_GWP_p_kWh,
                                      Biopower_GWP_p_kWh, Gas_GWP_p_kWh, Oil_GWP_p_kWh, Coal_GWP_p_kWh, Nuclear_PWR_GWP_p_kWh])

Prognostic_2030_with_CC_GWP_p_kWh = np.array([Solar_ground_GWP_p_kWh, Wind_onshore_GWP_p_kWh, Hydro_near_GWP_p_kWh,
                                              Biopower_GWP_p_kWh, Gas_cc_GWP_p_kWh, Oil_cc_GWP_p_kWh, Coal_cc_GWP_p_kWh, Nuclear_PWR_GWP_p_kWh])

Shares_Prognostic_2050 = np.array([Solar_2050, Wind_2030, Hydro_2050, Biopower_2050, Gas_2050, Oil_2050, Coal_2050, Nuclear_2050])/100

Prognostic_2050_GWP_p_kWh = np.array([Solar_ground_GWP_p_kWh, Wind_onshore_GWP_p_kWh, Hydro_near_GWP_p_kWh,
                                      Biopower_GWP_p_kWh, Gas_GWP_p_kWh, Oil_GWP_p_kWh, Coal_GWP_p_kWh, Nuclear_PWR_GWP_p_kWh])
Prognostic_2050_with_CC_GWP_p_kWh = np.array([Solar_ground_GWP_p_kWh, Wind_onshore_GWP_p_kWh, Hydro_near_GWP_p_kWh,
                                              Biopower_GWP_p_kWh, Gas_cc_GWP_p_kWh, Oil_cc_GWP_p_kWh, Coal_cc_GWP_p_kWh, Nuclear_PWR_GWP_p_kWh])

Shares_wo_HC = np.array([Solar_wo_HC, Wind_wo_HC, Hydro_wo_HC, Biopower_wo_HC, Gas_wo_HC, Oil_wo_HC, Coal_wo_HC, Nuclear_wo_HC])/100
Homebaked_wo_HC_GWP_p_kWh = np.array([Solar_ground_GWP_p_kWh, Wind_onshore_GWP_p_kWh, Hydro_near_GWP_p_kWh,
                                      Biopower_GWP_p_kWh, Gas_GWP_p_kWh, Oil_GWP_p_kWh, Coal_GWP_p_kWh, Nuclear_PWR_GWP_p_kWh])

# Aggregate
Euro_mix_GWP_p_kWh_agg = sum(Shares_Euro_2019 * Euro_mix_GWP_p_kWh)
Euro_mix_with_CC_GWP_p_kWh_agg = sum(Shares_Euro_2019 * Euro_mix_with_CC_GWP_p_kWh)

Prognostic_2030_GWP_p_kWh_agg = sum(Shares_Prognostic_2030*Prognostic_2030_GWP_p_kWh)
Prognostic_2030_with_CC_GWP_p_kWh_agg = sum(Shares_Prognostic_2030*Prognostic_2030_with_CC_GWP_p_kWh)

Prognostic_2050_GWP_p_kWh_agg = sum(Shares_Prognostic_2050*Prognostic_2050_GWP_p_kWh)
Prognostic_2050_with_CC_GWP_p_kWh_agg = sum(Shares_Prognostic_2050*Prognostic_2050_with_CC_GWP_p_kWh)

Homebaked_wo_HC_GWP_p_kWh_agg = sum(Shares_wo_HC*Homebaked_wo_HC_GWP_p_kWh)

print('Euro Mix 2019', Euro_mix_GWP_p_kWh_agg, 'gCO2-eq/kWh')
print('Euro Mix 2019 with CC', Euro_mix_with_CC_GWP_p_kWh_agg, 'gCO2-eq/kWh')

print('Prognostic 2030', Prognostic_2030_GWP_p_kWh_agg, 'gCO2-eq/kWh')
print('Prognostic 2030 with CC', Prognostic_2030_with_CC_GWP_p_kWh_agg, 'gCO2-eq/kWh')

print('Prognostic 2050', Prognostic_2050_GWP_p_kWh_agg, 'gCO2-eq/kWh')
print('Prognostic 2050 with CC', Prognostic_2050_with_CC_GWP_p_kWh_agg, 'gCO2-eq/kWh')

print('Homebaked without Hydrocarbons', Homebaked_wo_HC_GWP_p_kWh_agg, 'gCO2-eq/kWh')

# Producing 1 kg of Hydrogen
Electrolysis_kWh_p_kg = 5.0     # range 4.5 to 5.5
Euro_2019_electrolysis = Euro_mix_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Euro_2019_CC_electrolysis = Euro_mix_with_CC_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Prognostic_2030_electrolysis = Prognostic_2030_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Prognostic_2030_CC_electrolysis = Prognostic_2030_with_CC_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Prognostic_2050_electrolysis = Prognostic_2050_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Prognostic_2050_CC_electrolysis = Prognostic_2050_with_CC_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Homebaked_wo_HC_electrolysis = Homebaked_wo_HC_GWP_p_kWh_agg * Electrolysis_kWh_p_kg

Hydrogen_electrolysis = [Euro_2019_electrolysis, Euro_2019_CC_electrolysis, Prognostic_2030_electrolysis,
                         Prognostic_2030_CC_electrolysis, Prognostic_2050_electrolysis, Prognostic_2050_CC_electrolysis,
                         Homebaked_wo_HC_electrolysis]
X_axis = ['2019', '2019 with CC', '2030',
                         '2030 with CC', '2050', '2050 with CC',
                         'without HC']

plt.figure()
plt.bar(X_axis, Hydrogen_electrolysis)
plt.ylabel('gCO2-eq/kgH2')
plt.grid()

plt.figure()
plt.plot([2019, 2030, 2050], [Euro_2019_electrolysis, Prognostic_2030_electrolysis, Prognostic_2050_electrolysis])
plt.plot([2019, 2030, 2050], [Euro_2019_CC_electrolysis, Prognostic_2030_CC_electrolysis, Prognostic_2050_CC_electrolysis])
plt.plot([2019, 2050], [Homebaked_wo_HC_electrolysis, Homebaked_wo_HC_electrolysis], ls='--')
plt.legend(['European prognostic', 'With CC', 'Renewables based'])
plt.grid()
plt.xlim(2019, 2050)
plt.ylim(0, 1500)
plt.ylabel('gCO2-eq/kgH2')
plt.show()


