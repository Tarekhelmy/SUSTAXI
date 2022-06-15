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

'''
print('Euro Mix 2019', Euro_mix_GWP_p_kWh_agg, 'gCO2-eq/kWh')
print('Euro Mix 2019 with CC', Euro_mix_with_CC_GWP_p_kWh_agg, 'gCO2-eq/kWh')

print('Prognostic 2030', Prognostic_2030_GWP_p_kWh_agg, 'gCO2-eq/kWh')
print('Prognostic 2030 with CC', Prognostic_2030_with_CC_GWP_p_kWh_agg, 'gCO2-eq/kWh')

print('Prognostic 2050', Prognostic_2050_GWP_p_kWh_agg, 'gCO2-eq/kWh')
print('Prognostic 2050 with CC', Prognostic_2050_with_CC_GWP_p_kWh_agg, 'gCO2-eq/kWh')

print('Homebaked without Hydrocarbons', Homebaked_wo_HC_GWP_p_kWh_agg, 'gCO2-eq/kWh')
'''
# Producing 1 kg of Hydrogen with Electrolysis
Electrolysis_kWh_p_kg = 5.0 / 0.0841    # range 4.5 to 5.5
Euro_2019_electrolysis = Euro_mix_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Euro_2019_CC_electrolysis = Euro_mix_with_CC_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Prognostic_2030_electrolysis = Prognostic_2030_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Prognostic_2030_CC_electrolysis = Prognostic_2030_with_CC_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Prognostic_2050_electrolysis = Prognostic_2050_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Prognostic_2050_CC_electrolysis = Prognostic_2050_with_CC_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Homebaked_wo_HC_electrolysis = Homebaked_wo_HC_GWP_p_kWh_agg * Electrolysis_kWh_p_kg
Wind_energy_electrolysis = Wind_offshore_GWP_p_kWh * Electrolysis_kWh_p_kg

# Producing 1 kg of Hydrogen with NGSR
NSGR_Canada = 11893

# Producing 1 kg of Hydrogen with Coal Gasification
CG_Canada = 11299

Hydrogen_electrolysis = [Euro_2019_electrolysis, Euro_2019_CC_electrolysis, Prognostic_2030_electrolysis,
                         Prognostic_2030_CC_electrolysis, Prognostic_2050_electrolysis, Prognostic_2050_CC_electrolysis,
                         Homebaked_wo_HC_electrolysis]
X_axis = ['2019', '2019 with CC', '2030',
                         '2030 with CC', '2050', '2050 with CC',
                         'without HC']

# Hydrogen Leaks
H2_consumption_paxkm = 0.03578      # kg/(pax.km)
leaked_frac = 0.015      # 1 percent
H2_Carbon_eq = 11       # kg CO2/kgH2
leaks_impact = H2_consumption_paxkm*leaked_frac*H2_Carbon_eq * 1000     # g CO2/(pax.km)
#print(leaks_impact)

# Hydrogen cooling
Cooling_energy = 0.097 / 0.6        # efficiency added
Cooling_impact = Cooling_energy*Euro_mix_GWP_p_kWh_agg*H2_consumption_paxkm     # g CO2/(pax.km)
#print(Cooling_impact)

# Sustaxi Impact
gCO2_p_paxkm = np.array([Euro_2019_electrolysis, Prognostic_2030_electrolysis, Prognostic_2050_electrolysis])*H2_consumption_paxkm
gCO2_p_paxkm_CC = np.array([Euro_2019_CC_electrolysis, Prognostic_2030_CC_electrolysis, Prognostic_2050_CC_electrolysis])*H2_consumption_paxkm
gCO2_p_paxkm_wo_HC = Homebaked_wo_HC_electrolysis*H2_consumption_paxkm
gCO2_p_paxkm_ngsr = NSGR_Canada*H2_consumption_paxkm
gCO2_p_paxkm_cg = CG_Canada*H2_consumption_paxkm
print('Normal', gCO2_p_paxkm)
print('NGSR', gCO2_p_paxkm_ngsr)
print('Coal Gas', gCO2_p_paxkm_cg)
print(gCO2_p_paxkm_wo_HC)
# Reference Aircraft - Fuel consumption
King_air_200 = 1184/2606/4
Phenom_100 = 1273/1850/4
Mustang = 875/1330/4
Pc_12 = 1227/2978/4

# Reference Aircraft - CO2 emissions
kerosene_impact_kgCO2_p_kg = (3.16 + 0.5)*1000
King_air_200_gCO2_p_paxkm = King_air_200*kerosene_impact_kgCO2_p_kg
Phenom_100_gCO2_p_paxkm = Phenom_100*kerosene_impact_kgCO2_p_kg
Mustang_gCO2_p_paxkm = Mustang*kerosene_impact_kgCO2_p_kg
Pc_12_gCO2_p_paxkm = Pc_12*kerosene_impact_kgCO2_p_kg


plt.figure()
#plt.bar(X_axis, Hydrogen_electrolysis)
plt.bar(['Electrolysis, EU 2019', 'Renewables', 'NGSR', 'Coal Gas'],
        [Euro_2019_electrolysis, Homebaked_wo_HC_electrolysis, NSGR_Canada, CG_Canada], color=['blue', 'blue', 'red', 'grey'])
#plt.bar(, NSGR_Canada, color='red')
#plt.bar(, CG_Canada, color='grey')
plt.ylabel('gCO2-eq/kgH2')
#plt.xticks(rotation=45)
plt.yticks(np.arange(0, 18001, 2000))
plt.grid(axis='y')

plt.figure()
plt.plot([2019, 2030, 2050], [Euro_2019_electrolysis, Prognostic_2030_electrolysis, Prognostic_2050_electrolysis])
plt.plot([2019, 2030, 2050], [Euro_2019_CC_electrolysis, Prognostic_2030_CC_electrolysis, Prognostic_2050_CC_electrolysis])
plt.plot([2019, 2050], [Homebaked_wo_HC_electrolysis, Homebaked_wo_HC_electrolysis], ls='--')
plt.legend(['European prognosis', 'With CC', 'Renewables based'])
plt.xlim(2019, 2050)
plt.ylim(0, 18000)
plt.ylabel('gCO2-eq/kgH2')
plt.grid()

plt.figure()
plt.plot([2019, 2030, 2050], gCO2_p_paxkm)
plt.plot([2019, 2030, 2050], gCO2_p_paxkm_CC)
plt.plot([2019, 2050], [gCO2_p_paxkm_wo_HC, gCO2_p_paxkm_wo_HC])
plt.plot([2019, 2050], [King_air_200_gCO2_p_paxkm, King_air_200_gCO2_p_paxkm], color='red', ls='--')
plt.plot([2019, 2050], [Mustang_gCO2_p_paxkm, Mustang_gCO2_p_paxkm], color='yellow', ls='--')
plt.plot([2019, 2050], [Phenom_100_gCO2_p_paxkm, Phenom_100_gCO2_p_paxkm], color='grey', ls='--')
plt.plot([2019, 2050], [Pc_12_gCO2_p_paxkm, Pc_12_gCO2_p_paxkm], color='green', ls='--')
plt.legend(['Sustainable Air Taxi Prognosis', 'Prognosis with CC','Sustainable Air Taxi Renewables',
            'King air 200', 'Citation Mustang', 'Phenom 100', 'Pc-12'], loc='lower right')
plt.grid()
plt.xlim(2019, 2050)
plt.ylim(0, 700)
plt.xlabel('Year')
plt.ylabel('gCO2-eq/pax/km')
plt.show()


