#!/usr/bin/python
# coding: utf-8

""" This file contains the InputDialog class """

import logging
import tkinter
from tkinter.ttk import Label, Entry, Checkbutton, Button

from ranalysis.log.loghandler import logger


class InputDialog:
    """ Display input dialog for csv reading options

    Attributes
    ----------
    parent : tkinter.Frame
        the parent frame of the InputDialog

    Methods
    -------
    submit()
        submit_button action to submit entry options and destroy the frame
    get_input_options()
        get entry options
    """

    def __init__(self, parent):
        """ InputDialog constructor """
        top = self.top = tkinter.Toplevel(parent)
        self.__entry_label = Label(top, text='Delimiter of the csv file:')
        self.__entry_label.grid(row=1, column=1, rowspan=1, padx=5, pady=5)
        self.__entry_box = Entry(top)
        self.__entry_box.grid(row=1, column=2, rowspan=1, padx=5, pady=5)
        self.__checkbox_var_unit = tkinter.IntVar()
        self.__checkbox_var_unit.set(1)
        self.__check_button_unit = Checkbutton(top, text="Unit in the csv file?", variable=self.__checkbox_var_unit)
        self.__check_button_unit.grid(row=2, column=1, rowspan=1, padx=5, pady=5)
        self.__checkbox_var_clear = tkinter.IntVar()
        self.__checkbox_var_clear.set(1)
        self.__check_button_clear = Checkbutton(top, text="Clear the data?", variable=self.__checkbox_var_clear)
        self.__check_button_clear.grid(row=2, column=2, rowspan=1, padx=5, pady=5)
        self.__submit_button = Button(top, text='Submit', command=self.submit, width=35)
        self.__submit_button.grid(row=3, column=1, columnspan=2, padx=5, pady=5)
        self.__input_options = {
            'delimiter': ';',
            'unit': 1,
            'clear': 1
        }

    def submit(self):
        """ Submit entry options and destroy the frame """
        if self.__entry_box.get():
            self.__input_options['delimiter'] = self.__entry_box.get()
        self.__input_options['unit'] = self.__checkbox_var_unit.get()
        self.__input_options['clear'] = self.__checkbox_var_clear.get()
        self.top.destroy()
        logger.log(logging.INFO, "[InputDialog] " + str(self.__input_options))

    def get_input_options(self):
        """ Get entry options """
        return self.__input_options
