#!/usr/bin/python
# coding: utf-8

""" This file contains the singleton PlotCreator class """

import logging
import re
import numpy as np

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
    string_to_function(string_function)
        return a math function from a string
    get_plots_dict()
        return the plot dictionary
    get_plot_from_stringify(plot_stringify):
        return plot from its stringify version
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
            self.__replacements = {
                "sin": "np.sin",
                "cos": "np.cos",
                "tan": "np.tan",
                "arcsin": "np.arcsin",
                "arccos": "np.arccos",
                "arctan": "np.arctan",
                "exp": "np.exp",
                "ln": "np.log",
                "sqrt": "np.sqrt",
                "mod": "np.mod",
                "^": "**",
                "pi": "np.pi"
            }

            self.__allowed_words = [
                "x",
                "sin",
                "cos",
                "tan",
                "arcsin",
                "arccos",
                "arctan",
                "exp",
                "ln",
                "sqrt",
                "mod",
                "round",
                "pi"
            ]

    def string_to_function(self, string_function):
        """ Evaluates the string and returns a function of x

        Parameters
        ----------
        string_function : str
            the string to eval

        Returns
        ------
        func
            the math function from string
        """
        # find all words and check if all are allowed:
        for word in re.findall('[a-zA-Z_]+', string_function):
            if word not in self.__allowed_words:
                logger.log(logging.DEBUG, "[PlotCreator] " + word + " is forbidden to use in math expression")
                raise ValueError(
                    '"{}" is forbidden to use in math expression'.format(word)
                )

        for old, new in self.__replacements.items():
            string_function = string_function.replace(old, new)

        def func(x):
            return eval(string_function)

        return func

    def get_plots_dict(self):
        """ Get plots dictionary

        Returns
        ------
        dict
            the plots dictionary
        """
        return self.__plots_dict

    def get_plot_from_stringify(self, plot_stringify):
        """ Get plot from its stringify version

                Parameters
                ----------
                plot_stringify : str
                    the stringify of a plot

                Returns
                ------
                plot
                    the plot
                """
        pattern = re.search('id=(.+?) ', plot_stringify)
        if pattern:
            found = int(pattern.group(1))
            return self.get_plot_from_id(found)

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

    def plot_from_function(self, function, xmin, xmax, discr, xlabel="", ylabel=""):
        """ Create a plot from a mathematic function

        Parameters
        ----------
        function : str
            the mathematic function
        xmin :  int
            the x min
        xmax : int
            the x max
        discr : int
            the discretization of the interval between xmin and xmax
        xlabel :  str
            the name of the x label
        ylabel : str
            the name of the y label

        Returns
        ------
        plot
            the plot
        """
        func = self.string_to_function(str(function))
        a = float(xmin)
        b = float(xmax)
        x_interval = np.linspace(a, b, int(discr)).tolist()
        fx = []
        for x in x_interval:
            fx.append(func(x))

        return self.plot_from_data(x_interval, fx, str(xlabel), str(ylabel))

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

    def plot_from_data(self, x_data, y_data, x_axis="", y_axis="", x_unit="", y_unit=""):
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
        """ Refresh the plots with new data

        Parameters
        ----------
        data_manager :  DataManager
            the data manager associated to the data
        """
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
