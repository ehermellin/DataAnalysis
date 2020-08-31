#!/usr/bin/python
# coding: utf-8

""" This file contains the CliHandler class """

import logging
import queue

import matplotlib.pyplot as plt
from matplotlib import style

from ranalysis.data.datamanager import DataManager
from ranalysis.log.loghandler import logger, QueueHandler
from ranalysis.plot.graph import graph_from_fieldname, graph_from_fieldnames, graph_from_function, graph_clear,\
    graph_compare_plot_from_fieldnames, graph_compare_plot_values_from_fieldnames


class CliHandler:
    """ A class used to automatize the plot of data

        Attributes
        ----------
        log_queue : Queue
            the queue used in the logger
        queue_handler : QueueHandler
            queue handler used in the logger
        __file_path : str
            the file path to the csv file
        __data_manager : DataManager
            the data manager used to read csv file

        Methods
        -------
        read_data(fil_path, options)
            read data from file_path with csv options
        show_from_function(function, xmin, xmax, discr, xlabel, ylabel)
            show plot from mathematic functions
        show_from_fieldname(x_fieldname, y_fieldname)
            show plot from data field name (x-axis and y-axis)
        show_from_fieldnames(x_fieldname, y_fieldnames)
            show plot from data field name (x-axis and multiple y-axis)
        show_diff_from_fieldnames(x_fieldname, y_fieldnames, values=False):
            show plot difference between two graph from fieldnames in a plt matplotlib object
        """

    def __init__(self, file_path, options=None):
        """ CliHandler constructor

        Parameters
        ----------
        file_path : str
            the file path to the csv file
        options : dict
            the options to read the csv file
        """
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        self.queue_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
        logger.addHandler(self.queue_handler)

        style.use('ggplot')
        self.__data_manager = None
        self.__file_path = file_path
        self.read_data(file_path, options)

    def read_data(self, file_path, options=None):
        """ Read data from file_path with csv options

        Parameters
        ----------
        file_path : str
            the file path to the csv file
        options : dict
            the options to read the csv file
        """
        logger.log(logging.INFO, "[CliHandler] Read data from " + file_path)
        if options is None:
            options = {'delimiter': ';', 'unit': 1}

        if self.__file_path:
            self.__data_manager = DataManager()
            self.__data_manager.read_csv_file(file_path, options)

    def show_from_function(self, function, xmin, xmax, discr, xlabel="", ylabel=""):
        """ Plot mathematic function

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
        """
        logger.log(logging.INFO, "[CliHandler] Plot function " + function)
        fig, ax = plt.subplots()
        graph_clear(ax)
        graph_from_function(ax, function, xmin, xmax, discr, xlabel, ylabel)
        plt.show()

    def show_from_fieldname(self, x_fieldname, y_fieldname):
        """ Plot data from fieldname in a plt matplotlib object

        Parameters
        ----------
        x_fieldname : str
            the fieldname of the x-axis variable to plot
        y_fieldname : str
            the fieldname of the y-axis variable to plot
        """
        if self.__data_manager is not None:
            logger.log(logging.INFO, "[CliHandler] Show from field name " + x_fieldname + " " + y_fieldname)
            fig, ax = plt.subplots()
            graph_clear(ax)
            graph_from_fieldname(ax, self.__data_manager, x_fieldname, y_fieldname)
            plt.show()
        else:
            logger.log(logging.INFO, "[CliHandler] No data to show")

    def show_from_fieldnames(self, x_fieldname, y_fieldnames):
        """ Plot multiple data from fieldnames in a plt matplotlib object

        Parameters
        ----------
        x_fieldname : str
            the fieldname of the x-axis variable to plot
        y_fieldnames : list(str)
            the list of fieldname of the y-axis variable to plot
        """
        if self.__data_manager is not None:
            logger.log(logging.INFO, "[CliHandler] Show from field names " + x_fieldname + " " + str(y_fieldnames))
            fig, ax = plt.subplots()
            graph_clear(ax)
            graph_from_fieldnames(ax, self.__data_manager, x_fieldname, y_fieldnames)
            plt.show()
        else:
            logger.log(logging.INFO, "[CliHandler] No data to show")

    def show_diff_from_fieldnames(self, x_fieldname, y_fieldnames, values=False):
        """ Plot difference between two graph from fieldnames in a plt matplotlib object

        Parameters
        ----------
        x_fieldname : str
            the fieldname of the x-axis variable to plot
        y_fieldnames : list(str)
            the list of fieldname of the y-axis variable for the two plot to compare
        values : boolean
            display the diff values on the graph
        """
        if self.__data_manager is not None:
            logger.log(logging.INFO, "[CliHandler] Show from field names " + x_fieldname + " " + str(y_fieldnames))
            fig, ax = plt.subplots()
            graph_clear(ax)
            graph_compare_plot_from_fieldnames(ax, self.__data_manager, x_fieldname, y_fieldnames)
            if values:
                graph_compare_plot_values_from_fieldnames(ax, self.__data_manager, x_fieldname, y_fieldnames, 0.1, True)
            plt.show()
        else:
            logger.log(logging.INFO, "[CliHandler] No data to show")
