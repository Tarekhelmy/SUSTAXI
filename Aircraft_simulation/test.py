from Stability import *
from mass_estimations import Aircraft
import numpy as np
AC = Aircraft()
#stability = Stability()
#stability.procedures()


# VNV on mass_estimations module
# ==| class I
# ====| Do a manual calculation and check if correct
# ====| 1. verify statistical calculation from existing datapoint
def test_regress():

    A = np.vstack([AC.MTOWstat, np.ones(len(AC.MTOWstat))]).transpose()
    m, c = np.linalg.lstsq(A, AC.OEWstat, rcond=None)[0]

    assert abs(AC.a - m) < 1e-6
    assert abs(AC.b - c) < 1e-6

# ====| 2. verify fuel calculation by hand
def test_fuel():

    AC.fuel_factor = 0.2
    AC.f_res = 0.1
    AC.w_mtow = 10000
    AC.iter = 1
    AC.class1()
    correct_answer = 0.2 * 1.1 * 10000 * 40 / 120


    assert abs(AC.w_fuel - correct_answer) < 1e-6

# ==| class II
# ==| manually work out a random mass estimation formula en check if correct
# ====| 1. verify flightcontrols weight
def test_flightcontrols():
    AC.length_fus.append(10)
    AC.b_w = 10
    AC.limit_factor = 1.5
    AC.limit_load = 2
    AC.w_oew = 5000
    AC.w_crew = 0
    correct_answer = 0.053 * 10 ** 1.536 * 10 ** 0.371 * (3 * 5000 * 1e-4) ** 0.8
    AC.class2()

    assert abs(AC.w_flightcontrols - correct_answer) < 1e-6

# ==| powertrain sizing
# ====| 1. set shaft power to zero and ensure all pt component masses except cooling become zero
def test_powertrain():
    AC.w_mtow = 0
    AC.powertrain_mass()

    c11 = 0.3389827
    c3 = (1 / AC.n_fc) - 1
    c2 = 2.856 * 10 ** -7 * AC.lamda_o2 * AC.c_p_air * (AC.T_t2 - AC.T_t1) / (AC.n_ee * AC.n_fc)
    c12 = 1.215221

    correct_ans = c12 / (1 - (c11 * c3 + c2))
    correct_ans *= AC.watts_to_horsepower

    assert abs(AC.m_electric_engine - 0) < 1e-6
    assert abs(AC.fc_power - correct_ans) < 1e-6


# ==| iterations
# ====| increase a constant weight and check the snowball effect
# ====| add w_battery 50 kg and check more than 50 kg is added to the mtow due to snowball effect.
def test_snowball():

    # set up a default aircraft and perform design iterations
    ACdef = Aircraft()
    ACdef.classiter()
    ACdef.classiter2()
    ACdef.cgcalc()

    # set up an aircraft with a heavier (constant) battery and perform design iterations
    AChbat = Aircraft()
    AChbat.w_battery = 100
    diff = 100 - ACdef.w_battery
    AChbat.classiter()
    AChbat.classiter2()
    AChbat.cgcalc()

    # Verify that the weight gain did the snowball thing
    assert AChbat.MTOW - ACdef.MTOW > diff

# VNV on CG module
# ==| Set a bunch of masses to zero and manually verify the cg it finds
# ====| only do the cabin and verify the cg is in fact the cabin cg
def test_cg():

    #Just setting up cg properly
    cg = CenterOfGravity()
    cg.updatecg()
    cg.weight = cg.cg_lists()
    cg.weights = cg.weight[0]
    cg.fus_cg_locations = cg.weight[1]
    cg.wing_cg_locations = cg.weight[2]
    cg.mac = cg.weight[3]
    #Setting masses to 0 except fuselage, mtow (so massfractions still make sense)
    for entry in cg.weights:
        if entry != "fuselage":
            cg.weights[entry] = 0
    
    # cg.massfraction()

    #Run function to be tested
    cg.lemac_oew_pl_fuel()

    #In the end, the operational empty weight cg should just be the fuselage cg
    assert (cg.locations['oew'] == cg.fus_cg_locations['fuselage'])




# VNV on S&C module
# ==| Inspect plot and final solution with printed cg extremes
# ====|



