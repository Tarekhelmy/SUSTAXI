# SUSTAXI


This repository containts all code that is used in the design process of the SUSTAXI aircraft.
The tools include sizings, stability analysis, structural analysis, wing bending and lift distribution analysis etc.

### Aircraft_simulation ###

### Wing_Power_Loading.py ###
The Wing_Power_Loading.py file uses aerodynamic data and statistics to find a reasonable design point for the SUSTAXI aircraft.

### mass_estimations.py ###
The mass_estimations.py file uses the tools and iterates between class I and class II mass estimations to achieve a converged weight of the design.

### fuel_cell_optimization.py ###
The fuel_cell_optimization.py file uses data from literature to estimate the efficiency and power density of the desired fuel cells to be used as propulsion for the SUSTAXI. It uses the data stored in eff_prat and prat_mrat .csv files.

### cg_calculator.py ###
The cg_calculator.py file uses the converged weight that was found previously in order to estimate the center of gravity location of the SUSTAXI.

### Stability.py ###
The Stability.py file is concerned with the stability and controlability aspects of the SUSTAXI. It creates the scissor plot.

### V_n_diagram.py ###
The V_n_diagram.py file creates the flight envelope of the SUSTAXI.

### Aero_Tools ###

### You can explain here what your files do because I don't exactly know what's happening there :))) (FOR JULIEN)
