#!/usr/bin/python
# coding: utf-8

import re

from plot.plot import Plot


class PlotFactory:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if PlotFactory.__instance is None:
            PlotFactory()
        return PlotFactory.__instance

    def __init__(self):
        if PlotFactory.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            PlotFactory.__instance = self
            self.__plot_list = {}
            self.__counter = 0

    def plot_from_data(self, x_data, y_data, x_axis, y_axis, x_unit="", y_unit=""):
        plot = Plot(self.__counter, x_data, y_data, x_axis, y_axis, x_unit, y_unit)
        self.__plot_list[self.__counter] = plot
        self.__counter += 1
        return plot

    def matplotlib_from_plot(self, ax, plot_ids, parameters_dict):
        ax.clear()
        list_plots = []
        for plot_id in plot_ids:
            pattern = re.search('id=(.+?) ', plot_id)
            if pattern:
                found = int(pattern.group(1))
                list_plots.append(self.__plot_list[found])

        x_data = list_plots[0].get_x()
        ax.set_xlabel(list_plots[0].get_x_axis() + " [" + list_plots[0].get_x_unit() + "]")

        for plot in list_plots:
            label = plot.get_y_axis() + "(" + plot.get_y_unit() + ")"
            ax.plot(x_data, plot.get_y(), label=label, alpha=0.50)

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10), ncol=5, fancybox=True)
