V_jet = 194.44 #[m/s]
R = 2365 * 1000 #[m]
E_jet = R / V_jet #[s]
V_prop = 156 #[m/s]
E_prop = R / V_prop #[s]

L_D_jet_cruise = 12
L_D_jet_loiter = 14
L_D_prop_cruise = 13
L_D_prop_loiter = 16
# ALL taken from Roskam (needs to be computed though)

jet_fractions = 0.990 * 0.995 * 0.995 * 0.98 * 0.99 * 0.992 #[from Roskam]
prop_fractions = 0.992 * 0.996 * 0.996 * 0.990 * 0.992 * 0.992 #[from Roskam]

pre_cruise_fractions_jet = 0.990 * 0.995 * 0.995 * 0.98
pre_cruise_fractions_prop = 0.992 * 0.996 * 0.996 * 0.990

MTOW_jet = [28660, 18740, 38800, 22850, 25500, 11850, 13300, 20000, 19300, 13300, 15000, 68200, 43750, 14630, 24000, 4550, 18000, 20280, 10600, 10580, 10100, 10700, 10700] #[lb]
OEW_jet = [16600, 10760, 19840, 12300, 12845, 6605, 7196, 10951, 12130, 7064, 7650, 38750, 23828, 9100, 13400, 2408, 10650, 11775, 6770, 7195, 6580, 7203, 6990] #[lb]
# Reference business jet aircraft weights taken from Roskam

MTOW_prop = [14330, 16424, 46500, 22900, 25700, 12500, 15245, 11300, 12500, 8200, 9850, 14500, 36000, 8500, 45000, 34720, 5732, 7054, 28660, 44000, 41000, 21165, 26000, 9000] #[lb]
OEW_prop = [7716, 9072, 26560, 14175, 16075, 7750, 8500, 6494, 7538, 4915, 5682, 8387, 23693, 4613, 25525, 20580, 3245, 4299, 16094, 27000, 24635, 11945, 15510,  5018] #[lb]
# Reference regional turboprop aircraft weights taken from Roskam

# MTOW_prop = [3900, 5100, 6775, 9650, 5150, 5990, 6850, 6750, 7450, 8200, 6500, 7000, 5500, 3800, 3800, 8700, 3050, 2183, 9480, 10325, 7350, 2900] #[lbs]
# OEW_prop = [2466, 3236, 4423, 5765, 3305, 3948, 4077, 4368, 4668, 4915, 4003, 4221, 3737, 2354, 2430, 4910, 2100, 1322, 5732, 6629, 4100, 1610] #[lbs]
# Reference twin engine prop aircraft weights taken from Roskam

# design 1: 0.01143374625 / 3600
example_design = {"jet": True, "V": 250, "c": 19e-6, "L/Dcruise": 11, "L/Dloiter": 13, "fractions": jet_fractions, "R": 6400 * 1000, "E": 60 * 60, "Design no.": "example"}

design_1 = {"jet": True, "V": V_jet, "c": 11e-6, "L/Dcruise": L_D_jet_cruise, "L/Dloiter": L_D_jet_loiter, "fractions": jet_fractions, "R": R, "E": E_jet, "Design no.": "I"}

# design_2 = {"jet": False, "V": V_prop, "c": 0.014221077424 / 3600, "L/Dcruise": L_D_prop_cruise, "L/Dloiter": L_D_prop_loiter, "fractions": prop_fractions, "R": R, "E": E, "efficiency": 0.85, "Design no.": "II"}

design_3 = {"jet": True, "V": V_jet, "c": 11e-6, "L/Dcruise": L_D_jet_cruise, "L/Dloiter": L_D_jet_loiter, "fractions": jet_fractions, "R": R, "E": E_jet, "Design no.": "III"}

design_4 = {"jet": True, "V": V_jet, "c": 11e-6, "L/Dcruise": L_D_jet_cruise, "L/Dloiter": L_D_jet_loiter, "fractions": jet_fractions, "R": R, "E": E_jet, "Design no.": "IV"}

design_5 = {"jet": False, "V": V_prop, "c": 9e-8, "L/Dcruise": L_D_prop_cruise, "L/Dloiter": L_D_prop_loiter, "fractions": prop_fractions, "R": R, "E": E_prop, "efficiency": 0.85, "Design no.": "V"}

design_6 = {"jet": False, "V": V_prop, "c": 9e-8, "L/Dcruise": L_D_prop_cruise, "L/Dloiter": L_D_prop_loiter, "fractions": prop_fractions, "R": R, "E": E_prop, "efficiency": 0.85, "Design no.": "VI"}

designs = [example_design, design_1, design_3, design_4, design_5, design_6]

# 0.504 / 3600 / 1000
# print(0.0114 / 3600)