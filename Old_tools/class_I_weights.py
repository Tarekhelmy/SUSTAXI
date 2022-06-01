import numpy as np
from design_dictionaries import *
from scipy.stats import linregress
import matplotlib.pyplot as plt

### REFERENCE AIRCRAFT: ###
# Cessna Citation Mustang
# Cessna Citation CJ1 Flying
# Embraer Phenom 100
# King Air C90
# HondaJet Elite HA-420
# Cessna Citaion M2

g = 9.81  # [m/s]
lb_to_kg = 0.45359237  # converion rate
W_payload = 0 * g  # [N] #Payload weight (requirement)
W_crew = 2 * (170 + 30) * lb_to_kg * g  # [N] #[2 pilots] #weight taken from AIA regulations
f_res = 0.2  # [20% of fuel] #[fuel + fuel reserves]


def get_lin_reg_coefficients(dic):
    if dic["jet"]:
        return linregress(MTOW_jet, OEW_jet).slope, linregress(MTOW_jet, OEW_jet).intercept
        # Get the least-squares regression coefficients for business jets
    else:
        return linregress(MTOW_prop, OEW_prop).slope, linregress(MTOW_prop, OEW_prop).intercept
        # Get the least-squares regression coefficients for regional turbo-props


def plot_lin_regress(MTOW, OEW):
    # Plots the least-squares regression
    regr = linregress(MTOW, OEW)
    curve = [regr.slope * i + regr.intercept for i in MTOW]
    plt.plot(MTOW, OEW, "bo")
    plt.plot(MTOW, curve, "r--")
    plt.show()


def get_fuel_coefficient(dic):
    if dic["jet"]:
        cruise_fraction = np.exp(
            dic["R"] / (dic["V"] / (g * dic["c"]) * dic["L/Dcruise"]))  # Breguet Range equation for jets
        f1 = 1 / cruise_fraction

        loiter_fraction = np.exp(
            dic["E"] / ((1 / (g * dic["c"])) * dic["L/Dloiter"]))  # Breguet Endurance equation for jets
        f2 = 1 / loiter_fraction

    else:
        cruise_fraction = np.exp(
            dic["R"] / (dic["efficiency"] / (g * dic["c"]) * dic["L/Dcruise"]))  # Breguet Range equation for props
        f1 = 1 / cruise_fraction

        loiter_fraction = np.exp(dic["E"] / ((dic["efficiency"] / (dic["V"] * g * dic["c"])) * dic[
            "L/Dloiter"]))  # Breguet Endurance equation for props
        f2 = 1 / loiter_fraction

    # print(f1, f2)
    M_ff = f1 * f2 * dic["fractions"]  # Fuel fraction over entire mission duration
    # print(1 - M_ff)
    return (1 - M_ff)


def class_I_weight(dic):
    slope, intercept = get_lin_reg_coefficients(dic)[0], get_lin_reg_coefficients(dic)[1]
    intercept *= lb_to_kg * g  # [to N]

    fuel_coeff = get_fuel_coefficient(dic)

    W_TO = (W_payload + intercept + W_crew) / (
                1 - slope - fuel_coeff * (1 + f_res))  # Take-off weight is W_TO = W_E + W_crew + W_PL + W_F
    # W_tfo not taken into account at this stage of development

    W_empty = slope * W_TO + intercept  # Aircraft standard empty weight
    W_fused = fuel_coeff * W_TO  # Used fuel weight
    W_fuel = fuel_coeff * (1 + f_res) * W_TO  # Total fuel weight (W_fused + W_freserve)
    # W_fuel = W_TO - W_empty - W_crew - W_payload
    W_OE = W_empty + W_crew  # Operational empty weight
    # W_tfo = 0.001 * W_TO

    return W_TO, W_OE, W_fuel,  # W_tfo


# print(get_fuel_coefficient(design_1))

def get_range_diagram():
    tow_jet = 6524.1
    fuel_jet = 540
    reserve = fuel_jet * 0.2
    oew_jet = 4984.1
    payload = 1000
    harmonic_payload = 600
    harmonic_range = 1200
    other_range = 2475.95
    ferry_range = 3000

    oew_jets = [oew_jet, oew_jet]

    mtow_jet1 = [oew_jet + payload + reserve, tow_jet]
    mtow_jet2 = [tow_jet, tow_jet]
    mtow_jet3 = [tow_jet, tow_jet - harmonic_payload]

    reserve_array = [oew_jet + payload + reserve, oew_jet + payload + reserve]
    reserve_array2 = [oew_jet + payload + reserve, oew_jet + payload + reserve - (payload - harmonic_payload)]
    reserve_array3 = [oew_jet + payload + reserve - (payload - harmonic_payload), oew_jet + reserve]

    W_pl1 = np.array([payload, payload]) + oew_jet
    W_pl2 = np.array([payload, harmonic_payload]) + oew_jet
    W_pl3 = np.array([harmonic_payload, 0]) + oew_jet

    range1 = [0, harmonic_range]
    range2 = [harmonic_range, other_range]
    range3 = [0, ferry_range]
    ferry = [other_range, ferry_range]

    y = [0, tow_jet]
    x1 = [0, 0]
    x2 = [harmonic_range, harmonic_range]
    x3 = [other_range, other_range]
    x4 = [ferry_range, ferry_range]

    plt.figure(1)
    plt.grid()
    plt.title("Design 5 Payload-Range Diagram (Iteration 2)")
    plt.plot(range1, W_pl1, "green", linestyle="solid", marker="o")
    plt.plot(range2, W_pl2, "green", linestyle="solid", marker="o")
    plt.plot(ferry, W_pl3, "green", linestyle="solid", marker="o", label="Payload")

    plt.plot(range1, mtow_jet1, 'black', linestyle="-")
    plt.plot(range2, mtow_jet2, 'black', linestyle="-")
    plt.plot(ferry, mtow_jet3, 'black', linestyle="-", label="Take-off weight")

    plt.plot(range3, oew_jets, "blue", label="Operational Empty")

    plt.plot(range1, reserve_array, color="black", linestyle="--")
    plt.plot(range2, reserve_array2, color="black", linestyle="--")
    plt.plot(ferry, reserve_array3, color="black", linestyle="--", label="Payload + Fuel reserves")

    plt.plot(x1, y, color="green", linestyle="--", label="0 Range")
    plt.plot(x2, y, color="green", linestyle="--", label="Harmonic Range")
    plt.plot(x3, y, color="green", linestyle="--", label="Minimum Payload for Maximum Range")
    plt.plot(x4, y, color="green", linestyle="--", label="Ferry Range")

    plt.ylim(oew_jet - 100, tow_jet + 100)
    plt.xlabel("Range [km]")
    plt.ylabel("Weight [kg]")
    plt.legend(loc="upper right", fontsize="small")

    plt.show()
    plt.close()


def get_prop_range_diagram():
    tow_jet = 6500
    fuel_jet = 1515
    reserve = fuel_jet * 0.2
    oew_jet = 3985

    oew_jets = [oew_jet, oew_jet]

    mtow_jet1 = [oew_jet + 1000 + reserve, tow_jet]
    mtow_jet2 = [tow_jet, tow_jet]
    mtow_jet3 = [tow_jet, tow_jet - 600]

    reserve_array = [oew_jet + 1000 + reserve, oew_jet + 1000 + reserve]
    reserve_array2 = [oew_jet + 1000 + reserve, oew_jet + 1000 + reserve - 400]
    reserve_array3 = [oew_jet + 1000 + reserve - 400, oew_jet + reserve]

    range1 = [0, 1200]
    range2 = [1200, 1655]
    range3 = [0, 2000]
    ferry = [1655, 2000]

    W_pl1 = np.array([1000, 1000]) + oew_jet
    W_pl2 = np.array([1000, 600]) + oew_jet
    W_pl3 = np.array([600, 0]) + oew_jet

    y = [0, tow_jet]
    x1 = [0, 0]
    x2 = [1200, 1200]
    x3 = [1655, 1655]
    x4 = [2000, 2000]

    plt.figure(1)
    plt.grid()
    plt.title("Propeller Propulsion Payload-Range Diagram")
    plt.plot(range1, W_pl1, "green", linestyle="solid", marker="o")
    plt.plot(range2, W_pl2, "green", linestyle="solid", marker="o")
    plt.plot(ferry, W_pl3, "green", linestyle="solid", marker="o", label="Payload")

    plt.plot(range1, mtow_jet1, 'black', linestyle="-")
    plt.plot(range2, mtow_jet2, 'black', linestyle="-")
    plt.plot(ferry, mtow_jet3, 'black', linestyle="-", label="Take-off weight")

    plt.plot(range3, oew_jets, "blue", label="Operational Empty")

    plt.plot(range1, reserve_array, color="black", linestyle="--")
    plt.plot(range2, reserve_array2, color="black", linestyle="--")
    plt.plot(ferry, reserve_array3, color="black", linestyle="--", label="Payload + Fuel reserves")

    plt.plot(x1, y, color="green", linestyle="--", label="0 Range")
    plt.plot(x2, y, color="green", linestyle="--", label="Harmonic Range")
    plt.plot(x3, y, color="green", linestyle="--", label="Minimum Payload for Maximum Range")
    plt.plot(x4, y, color="green", linestyle="--", label="Ferry Range")

    plt.ylim(oew_jet - 100, tow_jet + 100)
    plt.xlabel("Range [km]")
    plt.ylabel("Weight [kg]")
    plt.legend(loc="upper right", fontsize="small")

    plt.show()
    plt.close()


# get_prop_range_diagram()
# get_range_diagram()


if __name__ == "__main__":
    # plot_lin_regress(MTOW_prop, OEW_prop)
    for design in designs:
        name = design["Design no."]
        print(
            f"DESIGN: {name} \nMaximum take-off weight: {class_I_weight(design)[0] / g} [kg], \nOperational empty weight: {class_I_weight(design)[1] / g} [kg], \nFuel weight: {class_I_weight(design)[2] / g} [kg]")
    # print(get_lin_reg_coefficients(design_5))