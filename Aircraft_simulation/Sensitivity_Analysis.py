import types

from Stability import  Stability
from cg_calculator import CenterOfGravity
# from V_n_diagram import VNDiagram
import numpy as np
import matplotlib.pyplot as plt
import ast



class Verification(Stability):
    def __init__(self):
        super().__init__()
        self.script()
        self.procedures()
        self.sensitive_attribute = dict()
        self.sensitive_iteration = 1
        self.sensitivity_parameter = 3
        self.starting_lemac = 25
        self.iterativelemac = self.starting_lemac
        self.percentage_change = 1


    def iterationthings(self,attr):
        self.mainprocedures()
        self.script()
        self.proceduresattr(attr)


    def tryloop(self,attr):
        try:
            self.iterationthings(attr)
        except:
            self.reset()
            self.iterativelemac += 1
            self.lemac = self.iterativelemac
            setattr(self, attr, value)
            self.tryloop(attr)

    def tryloopupdate(self,attr):
        try:
            self.iterationthings(attr)
        except:
            self.reset()
            self.iterativelemac += 1
            self.lemac = self.iterativelemac
            setattr(self, attr, value*(1+self.sensitivity_parameter/100))
            self.tryloop(attr)

    def sensitivity(self):
        global value
        for attr in dir(self) :
            if not attr.startswith('__') and \
                    type(getattr(self, attr))!=types.MethodType  and \
                    not type(getattr(self, attr)) is np.ndarray and not \
                    type(getattr(self, attr)) is list and not\
                    type(getattr(self, attr)) is None and not getattr(self, attr)==None \
                    and not type(getattr(self, attr)) is dict and attr!= "iter" and not \
                    type(getattr(self, attr)) is tuple and attr!= "meters_to_feet"  and \
                    attr!= "kgs_to_pounds"  and attr!= "watts_to_horsepower" :
                self.sensitive_iteration += 1
                self.reset()
                value = getattr(self, attr)
                self.tryloop(attr)
                originaloew = self.oew()
                value = getattr(self, attr)
                self.reset()
                self.iterativelemac = self.starting_lemac
                setattr(self, attr, value*(1+self.sensitivity_parameter/100))
                self.tryloopupdate(attr)
                newoew = self.oew()
                if abs(originaloew-newoew)/originaloew>=self.percentage_change/100:
                    self.sensitive_attribute[f'{attr}'] = abs(originaloew-newoew)/(originaloew)


    def sensitivity_table(self):
        for i in range(1,20,2):
            self.sensitivity_parameter = i
            self.sensitivity()
            print(f"for a sensitivity parameter of {i}, the following parameters are sensitive",self.sensitive_attribute)
        pass

    def convergencetest(self):

        pass

    def extremetest(self):

        pass
verification = Verification()
verification.sensitivity_table()