import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math


class BarChart:

    def __init__(self,
                 bars: np.ndarray,
                 handles: list[str],
                 names: list[str],
                 title: str):

        """
        :param bars: the bar data, each bar is a row
        :param handles: the bar section labels
        :param names: the x-labels of the bars
        :param title: the title of the plot

        additional info
        ---------------
        shiiit

        """

        self.data_matrix = pd.DataFrame(bars, index=names, columns=handles)
        self.title = title

    def plot_bar(self):
        self.data_matrix.plot(kind='bar', stacked=True, title=self.title, use_index=True, rot=0)
        plt.show()


if __name__ == "__main__":
    component_weights = np.array([[10, 20, 15, 30],
                                  [8, 22, 17, 25]])
    component_names = ['fuselage', 'payload', 'fuel', 'powertrain']
    aircraft_name = ['aircraft1', 'aircraft2']

    MassBuildup = BarChart(component_weights, component_names, aircraft_name, 'test title')
    MassBuildup.plot_bar()
