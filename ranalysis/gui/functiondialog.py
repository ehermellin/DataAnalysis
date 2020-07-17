#!/usr/bin/python
# coding: utf-8

""" This file contains the FunctionDialog class """

import logging
import tkinter
from tkinter.ttk import Label, Entry, Button

from ranalysis.log.loghandler import logger
from ranalysis.plot.plotcreator import PlotCreator


class FunctionDialog:
    """ Display function dialog for creating plot from math functions

    Attributes
    ----------
    parent : tkinter.Frame
        the parent frame of the FunctionDialog

    Methods
    -------
    create_plot_from_function()
        create the plot from math functions
    get_plot()
        get the plot
    quit()
        exit tht dialog
    """

    def __init__(self, parent, function="x*x", xmin=1.0, xmax=10.0, discr=100, xlabel="x", ylabel="x*x"):
        """ FunctionDialog constructor """
        top = self.top = tkinter.Toplevel(parent)
        self.__entry_function_label = Label(top, text='Enter the function:', width=25)
        self.__entry_function_label.grid(row=2, column=1, columnspan=2, rowspan=1, padx=5, pady=5)
        self.__entry_function = Entry(top, width=50)
        self.__entry_function.insert(tkinter.END, function)
        self.__entry_function.grid(row=2, column=3, columnspan=4, rowspan=1, padx=5, pady=5)

        self.__entry_xmin_label = Label(top, text='X min:', width=10)
        self.__entry_xmin_label.grid(row=3, column=1, columnspan=1, rowspan=1, padx=5, pady=5)
        self.__entry_xmin = Entry(top, width=10)
        self.__entry_xmin.insert(tkinter.END, xmin)
        self.__entry_xmin.grid(row=3, column=2, columnspan=1, rowspan=1, padx=5, pady=5)

        self.__entry_xmax_label = Label(top, text='X max:', width=10)
        self.__entry_xmax_label.grid(row=4, column=1, columnspan=1, rowspan=1, padx=5, pady=5)
        self.__entry_xmax = Entry(top, width=10)
        self.__entry_xmax.insert(tkinter.END, xmax)
        self.__entry_xmax.grid(row=4, column=2, columnspan=1, rowspan=1, padx=5, pady=5)

        self.__entry_discr_label = Label(top, text='Discr:', width=10)
        self.__entry_discr_label.grid(row=3, column=5, columnspan=1, rowspan=1, padx=5, pady=5)
        self.__entry_discr = Entry(top, width=10)
        self.__entry_discr.insert(tkinter.END, discr)
        self.__entry_discr.grid(row=3, column=6, columnspan=1, rowspan=1, padx=5, pady=5)

        self.__entry_xlabel_label = Label(top, text='X label:', width=10)
        self.__entry_xlabel_label.grid(row=3, column=3, columnspan=1, rowspan=1, padx=5, pady=5)
        self.__entry_xlabel = Entry(top, width=10)
        self.__entry_xlabel.insert(tkinter.END, xlabel)
        self.__entry_xlabel.grid(row=3, column=4, columnspan=1, rowspan=1, padx=5, pady=5)

        self.__entry_ylabel_label = Label(top, text='Y label:', width=10)
        self.__entry_ylabel_label.grid(row=4, column=3, columnspan=1, rowspan=1, padx=5, pady=5)
        self.__entry_ylabel = Entry(top, width=10)
        self.__entry_ylabel.insert(tkinter.END, ylabel)
        self.__entry_ylabel.grid(row=4, column=4, columnspan=1, rowspan=1, padx=5, pady=5)

        self.__plot_button = Button(top, text='Plot', command=self.create_plot_from_function, width=35)
        self.__plot_button.grid(row=5, column=1, columnspan=3, rowspan=1, padx=5, pady=5)

        self.__cancel_button = Button(top, text='Cancel', command=self.quit, width=35)
        self.__cancel_button.grid(row=5, column=4, columnspan=3, rowspan=1, padx=5, pady=5)

        self.__plot = None

    def create_plot_from_function(self):
        """ create plot from math functions """
        logger.log(logging.DEBUG, "[FunctionDialog] Creating plot from math function " + self.__entry_function.get())
        self.__plot = PlotCreator.get_instance().plot_from_function(self.__entry_function.get(),
                                                                    self.__entry_xmin.get(), self.__entry_xmax.get(),
                                                                    self.__entry_discr.get(), self.__entry_xlabel.get(),
                                                                    self.__entry_ylabel.get())

        self.__plot.set_function(str(self.__entry_function.get()))

        self.quit()

    def get_plot(self):
        """ Get the plot """
        return self.__plot

    def quit(self):
        """ Exit the dialog """
        self.top.destroy()
