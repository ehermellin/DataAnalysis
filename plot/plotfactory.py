#!/usr/bin/python
# coding: utf-8

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
            self.__plots_dict = {}
            self.__counter = 0

    def get_plots_dict(self):
        return self.__plots_dict

    def get_plot_from_id(self, plot_id):
        return self.__plots_dict[plot_id]

    def plot_factory(self, data_manager, x_data_name, y_data_names):
        plots_list = []
        for y_data_name in y_data_names:
            plot = self.plot_from_data(data_manager.get_data_from_field_name(x_data_name),
                                       data_manager.get_data_from_field_name(y_data_name),
                                       x_data_name,
                                       y_data_name,
                                       data_manager.get_unit_from_field_name(x_data_name),
                                       data_manager.get_unit_from_field_name(y_data_name))
            plots_list.append(plot)
        return plots_list

    def plot_from_data(self, x_data, y_data, x_axis, y_axis, x_unit="", y_unit=""):
        plot = Plot(self.__counter, x_data, y_data, x_axis, y_axis, x_unit, y_unit)
        self.__plots_dict[self.__counter] = plot
        self.__counter += 1
        return plot
