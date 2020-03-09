#!/usr/bin/python
# coding: utf-8

import logging
import matplotlib.pyplot as plt

from data.datamanager import DataManager
from log.loghandler import logger
from plot.graph import graph_from_fieldname, graph_from_fieldnames


class CliHandler:

    def __init__(self, filepath):
        self.__file_path = filepath
        self.__data_manager = DataManager()
        if self.__file_path:
            self.__data_manager.read_csv_file(filepath, {'delimiter': ';', 'unit': 1})

    def show_from_fieldname(self, x_fieldname, y_fieldname):
        fig, ax = plt.subplots()
        graph_from_fieldname(ax, self.__data_manager, x_fieldname, y_fieldname)
        plt.show()

    def show_from_fieldnames(self, x_fieldname, y_fieldnames):
        fig, ax = plt.subplots()
        graph_from_fieldnames(ax, self.__data_manager, x_fieldname, y_fieldnames)
        plt.show()
