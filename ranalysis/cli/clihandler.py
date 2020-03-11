#!/usr/bin/python
# coding: utf-8

""" This file contains the CliHandler class """

import logging
import queue

import matplotlib.pyplot as plt
from matplotlib import style

from ranalysis.data.datamanager import DataManager
from ranalysis.log.loghandler import logger, QueueHandler
from ranalysis.plot.graph import graph_from_fieldname, graph_from_fieldnames


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
        show_from_fieldname(x_fieldname, y_fieldname)
            show plot from data field name (x-axis and y-axis)
        show_from_fieldnames(x_fieldname, y_fieldnames)
            show plot from data field name (x-axis and multiple y-axis)
        """

    def __init__(self, file_path):
        """ CliHandler constructor

        Parameters
        ----------
        file_path : str
            the file path to the csv file
        """
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        self.queue_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
        logger.addHandler(self.queue_handler)

        style.use('ggplot')
        self.__file_path = file_path
        self.__data_manager = DataManager()
        if self.__file_path:
            self.__data_manager.read_csv_file(file_path, {'delimiter': ';', 'unit': 1})

    def show_from_fieldname(self, x_fieldname, y_fieldname):
        """ Plot data from fieldname in a plt matplotlib object

        Parameters
        ----------
        x_fieldname : str
            the fieldname of the x-axis variable to plot
        y_fieldname : str
            the fieldname of the y-axis variable to plot
        """
        logger.log(logging.INFO, "[CliHandler] show from field name " + x_fieldname + " " + y_fieldname)
        fig, ax = plt.subplots()
        graph_from_fieldname(ax, self.__data_manager, x_fieldname, y_fieldname)
        plt.show()

    def show_from_fieldnames(self, x_fieldname, y_fieldnames):
        """ Plot multiple data from fieldnames in a plt matplotlib object

        Parameters
        ----------
        x_fieldname : str
            the fieldname of the x-axis variable to plot
        y_fieldnames : list(str)
            the list of fieldname of the y-axis variable to plot
        """
        logger.log(logging.INFO, "[CliHandler] show from field names " + x_fieldname + " " + str(y_fieldnames))
        fig, ax = plt.subplots()
        graph_from_fieldnames(ax, self.__data_manager, x_fieldname, y_fieldnames)
        plt.show()
