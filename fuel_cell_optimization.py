import numpy as np
import matplotlib.pyplot as plt


class FuelCellSizing:

    def __init__(self, deg):
        """
        :param deg: int, Degree of the polynomial fit
        """
        self.y_prat = None
        self.x_mrat = None
        self.y_nu = None
        self.x_prat = None
        self.eff_prat_coeffs = None
        self.prat_mrat_coeffs = None
        self.eff_prat = None
        self.prat_mrat = None
        self.deg = deg

    def fit_plots(self):
        """
        description
        ----------
        make polynomial fits for the fuel cell sizing plots
        :return:
        """
        self.eff_prat = np.genfromtxt('eff_prat.csv', delimiter=',')
        self.prat_mrat = np.genfromtxt('prat_mrat.csv', delimiter=',')

        self.x_prat = self.eff_prat[:, 0]
        self.y_nu = self.eff_prat[:, 1]
        self.eff_prat_coeffs = np.polyfit(self.x_prat, self.y_nu, self.deg)

        self.x_mrat = self.prat_mrat[:, 0]
        self.y_prat = self.prat_mrat[:, 1]
        self.prat_mrat_coeffs = np.polyfit(self.x_mrat, self.y_prat, self.deg)

    def nu(self, prat):
        """
        :param prat: float, P divided by P_max
        :return nu: float, efficiency
        """

        nu_val = 0
        for n in reversed(range(self.deg + 1)):
            nu_val += self.eff_prat_coeffs[self.deg - n] * prat ** n
        return nu_val

    def prat(self, mrat):
        """
        :param mrat: float, m_storage divided by m_conversion
        :return prat: foat, P_max divided by P
        """

        prat_val = 0
        for n in reversed(range(self.deg + 1)):
            prat_val += self.prat_mrat_coeffs[self.deg - n] * mrat ** n
        return prat_val

    def plot(self):

        """
        Description
        ----------
        Plot the polyfit with the original datapoints to verify implementation is correct
        """

        self.fit_y_nu = self.nu(self.x_prat)
        self.fit_y_prat = self.prat(self.x_mrat)

        fig, (ax1, ax2) = plt.subplots(1, 2)
        ax1.plot(self.x_prat, self.y_nu, label='Image Points')
        ax1.plot(self.x_prat, self.fit_y_nu, label='Degree ' + str(self.deg) + ' Polynomial Fit')
        ax1.set_title('Efficiency as a function power ratio')
        ax1.legend()

        ax2.plot(self.x_mrat, self.y_prat, label='Image Points')
        ax2.plot(self.x_mrat, self.fit_y_prat, label='Degree ' + str(self.deg) + ' Polynomial Fit')
        ax2.set_title('Optimum power ratio as a function of mass ratio')
        ax2.legend()

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    FuelCell = FuelCellSizing(10)
    FuelCell.fit_plots()
    FuelCell.plot()
