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

    def plot_from_data(self, x_data, y_data, x_axis, y_axis):
        plot = Plot(self.__counter, x_data, y_data, x_axis, y_axis)
        self.__plot_list[self.__counter] = plot
        self.__counter += 1
        return plot

    def matplotlib_from_plot(self, ax, plot_ids, param_dict):
        ax.clear()
        for plot_id in plot_ids:
            pattern = re.search('id=(.+?) ', plot_id)
            if pattern:
                found = int(pattern.group(1))
                plot = self.__plot_list[found]
                ax.plot(plot.get_x(), plot.get_y(), **param_dict)
