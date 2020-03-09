#!/usr/bin/python
# coding: utf-8

import logging

from log.loghandler import logger
from plot.plot import Plot


class PlotCreator:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if PlotCreator.__instance is None:
            PlotCreator()
        return PlotCreator.__instance

    def __init__(self):
        if PlotCreator.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            PlotCreator.__instance = self
            self.__plots_dict = {}
            self.__counter = 0

    def get_plots_dict(self):
        return self.__plots_dict

    def get_plot_from_id(self, plot_id):
        return self.__plots_dict[plot_id]

    def plot_from_fieldname(self, data_manager, x_data_name, y_data_name):
        logger.log(logging.INFO, "[PlotCreator] Plot from fieldnames")
        plot = self.__create_plot(data_manager.get_data_from_field_name(x_data_name),
                                  data_manager.get_data_from_field_name(y_data_name),
                                  x_data_name,
                                  y_data_name,
                                  data_manager.get_unit_from_field_name(x_data_name),
                                  data_manager.get_unit_from_field_name(y_data_name))
        return plot

    def plot_from_fieldnames(self, data_manager, x_data_name, y_data_names):
        logger.log(logging.INFO, "[PlotCreator] Plot from multiple fieldnames")
        plots_list = []
        for y_data_name in y_data_names:
            plot = self.__create_plot(data_manager.get_data_from_field_name(x_data_name),
                                      data_manager.get_data_from_field_name(y_data_name),
                                      x_data_name,
                                      y_data_name,
                                      data_manager.get_unit_from_field_name(x_data_name),
                                      data_manager.get_unit_from_field_name(y_data_name))
            plots_list.append(plot)
        return plots_list

    def plot_from_data(self, x_data, y_data, x_axis, y_axis, x_unit="", y_unit=""):
        logger.log(logging.INFO, "[PlotCreator] Plot from data")
        plot = self.__create_plot(x_data, y_data, x_axis, y_axis, x_unit, y_unit)
        return plot

    def plot_from_multiple_data(self, x_data, y_multiple_data, x_axis, y_multiple_axis, x_unit="", y_unit=""):
        logger.log(logging.INFO, "[PlotCreator] Plot from multiple data")
        plots_list = []
        for i in range(len(y_multiple_data)):
            plots_list.append(self.__create_plot(x_data, y_multiple_data[i], x_axis, y_multiple_axis[i],
                                                 x_unit, y_unit))
        return plots_list

    def __create_plot(self, x_data, y_data, x_axis, y_axis, x_unit="", y_unit=""):
        plot = Plot(self.__counter, x_data, y_data, x_axis, y_axis, x_unit, y_unit)
        self.__plots_dict[self.__counter] = plot
        self.__counter += 1
        logger.log(logging.DEBUG, "[PlotCreator] Create plot " + str(plot))
        return plot
