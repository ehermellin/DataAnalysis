#!/usr/bin/python
# coding: utf-8

import logging
import queue

import matplotlib.pyplot as plt
from matplotlib import style

from ranalysis.data.datamanager import DataManager
from ranalysis.log.loghandler import logger, QueueHandler
from ranalysis.plot.graph import graph_from_fieldname, graph_from_fieldnames


class CliHandler:

    def __init__(self, filepath):
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        self.queue_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
        logger.addHandler(self.queue_handler)

        style.use('ggplot')
        self.__file_path = filepath
        self.__data_manager = DataManager()
        if self.__file_path:
            self.__data_manager.read_csv_file(filepath, {'delimiter': ';', 'unit': 1})

    def show_from_fieldname(self, x_fieldname, y_fieldname):
        logger.log(logging.INFO, "[CliHandler] show from field name " + x_fieldname + " " + y_fieldname)
        fig, ax = plt.subplots()
        graph_from_fieldname(ax, self.__data_manager, x_fieldname, y_fieldname)
        plt.show()

    def show_from_fieldnames(self, x_fieldname, y_fieldnames):
        logger.log(logging.INFO, "[CliHandler] show from field names " + x_fieldname + " " + str(y_fieldnames))
        fig, ax = plt.subplots()
        graph_from_fieldnames(ax, self.__data_manager, x_fieldname, y_fieldnames)
        plt.show()
