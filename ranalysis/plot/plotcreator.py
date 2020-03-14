#!/usr/bin/python
# coding: utf-8

""" This file contains the singleton PlotCreator class """

import logging

from ranalysis.log.loghandler import logger
from ranalysis.plot.plot import Plot


class PlotCreator:
    """ A singleton class used to create Plot

    Attributes
    ----------
    __plots_dict : dict
        the dictionary used to store plot {id : plot}
    __counter :  int
        the counter used to create plot id

    Methods
    -------
    get_instance()
        return the instance of PlotCreator
    get_plots_dict()
        return the plot dictionary
    get_plot_from_id(plot_id)
        return a plot from the dictionary according to its id
    plot_from_fieldname(data_manager, x_data_name, y_data_name)
        create a plot from a variable fieldname
    plot_from_fieldnames(data_manager, x_data_name, y_data_names)
        create a list of plots from variable fieldnames
    plot_from_data(x_data, y_data, x_axis, y_axis, x_unit="", y_unit="")
        create a plot from a list of data
    plot_from_multiple_data(x_data, y_multiple_data, x_axis, y_multiple_axis, x_unit="", y_unit="")
        create a list of plots from multiple list of data
    refresh_plots()
        refresh all the plot
    __create_plot(x_data, y_data, x_axis, y_axis, x_unit="", y_unit="")
        create a plot
    """

    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if PlotCreator.__instance is None:
            PlotCreator()
        return PlotCreator.__instance

    def __init__(self):
        """ PlotCreator constructor"""
        if PlotCreator.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            PlotCreator.__instance = self
            self.__plots_dict = {}
            self.__counter = 0

    def get_plots_dict(self):
        """ Get plots dictionary

        Returns
        ------
        dict
            the plots dictionary
        """
        return self.__plots_dict

    def get_plot_from_id(self, plot_id):
        """ Get plot from the dictionary according to its id

        Parameters
        ----------
        plot_id : list(int)
            the plot id to get

        Returns
        ------
        plot
            the plot
        """
        return self.__plots_dict[plot_id]

    def plot_from_fieldname(self, data_manager, x_data_name, y_data_name):
        """ Create a plot from a variable fieldname

        Parameters
        ----------
        data_manager : DataManager
            the data_manager used to read csv file
        x_data_name :  str
            the name of the x variable
        y_data_name : str
            the name of the y variable

        Returns
        ------
        plot
            the plot
        """
        logger.log(logging.DEBUG, "[PlotCreator] Plot from fieldnames")
        plot = self.__create_plot(data_manager.get_data_from_field_name(x_data_name),
                                  data_manager.get_data_from_field_name(y_data_name),
                                  x_data_name,
                                  y_data_name,
                                  data_manager.get_unit_from_field_name(x_data_name),
                                  data_manager.get_unit_from_field_name(y_data_name))
        return plot

    def plot_from_fieldnames(self, data_manager, x_data_name, y_data_names):
        """ Create a list of plots from variable fieldnames

        Parameters
        ----------
        data_manager : DataManager
            the data_manager used to read csv file
        x_data_name :  str
            the name of the x variable
        y_data_names : list[str]
            the names of the y variables

        Returns
        ------
        list(plot)
            the list of plots
        """
        logger.log(logging.DEBUG, "[PlotCreator] Plot from multiple fieldnames")
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
        """ Create a plot from data

        Parameters
        ----------
        x_data :  list (int, float, ...)
            list of data (x-axis)
        y_data : list (int, float, ...)
            list of data (y-axis)
        x_axis : str
            the label of the x-axis
        y_axis : str
            the label of the y-axis
        x_unit : str
            the unit of the x-axis ("")
        y_unit : str
            the unit of the x-axis ("")

        Returns
        ------
        plot
            the plot
        """
        logger.log(logging.DEBUG, "[PlotCreator] Plot from data")
        plot = self.__create_plot(x_data, y_data, x_axis, y_axis, x_unit, y_unit)
        return plot

    def plot_from_multiple_data(self, x_data, y_multiple_data, x_axis, y_multiple_axis, x_unit="", y_unit=""):
        """ Create a list of plot from multiple data

        Parameters
        ----------
        x_data :  list (int, float, ...)
            list of data (x-axis)
        y_multiple_data : list (list(int, float, ...))
            multiple list of data (y-axis)
        x_axis : str
            the label of the x-axis
        y_multiple_axis : list(str)
            list of label of the y-axis
        x_unit : str
            the unit of the x-axis ("")
        y_unit : str
            the unit of the x-axis ("")

        Returns
        ------
        list(plot)
            the list of plot
        """
        logger.log(logging.DEBUG, "[PlotCreator] Plot from multiple data")
        plots_list = []
        for i in range(len(y_multiple_data)):
            plots_list.append(self.__create_plot(x_data, y_multiple_data[i], x_axis, y_multiple_axis[i],
                                                 x_unit, y_unit))
        return plots_list

    def refresh_plots(self, data_manager):
        logger.log(logging.DEBUG, "[PlotCreator] Refresh plots data")
        for plot in self.__plots_dict.values():
            if plot.get_x_axis() in data_manager.get_field_names() \
                    and plot.get_y_axis() in data_manager.get_field_names():
                plot.set_x(data_manager.get_data_from_field_name(plot.get_x_axis()))
                plot.set_y(data_manager.get_data_from_field_name(plot.get_y_axis()))

    def __create_plot(self, x_data, y_data, x_axis, y_axis, x_unit="", y_unit=""):
        """ Create a plot

        Parameters
        ----------
        x_data :  list (int, float, ...)
            list of data (x-axis)
        y_data : list (int, float, ...)
            list of data (y-axis)
        x_axis : str
            the label of the x-axis
        y_axis : str
            the label of the y-axis
        x_unit : str
            the unit of the x-axis ("")
        y_unit : str
            the unit of the x-axis ("")

        Returns
        ------
        plot
            the plot
        """
        plot = Plot(self.__counter, x_data, y_data, x_axis, y_axis, x_unit, y_unit)
        self.__plots_dict[self.__counter] = plot
        self.__counter += 1
        logger.log(logging.DEBUG, "[PlotCreator] Create plot " + str(plot))
        return plot
