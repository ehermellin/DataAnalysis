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
        the parent frame of the LoggerFrame

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
        self.__entry_label = Label(top, text='Enter the delimiter of the csv file:')
        self.__entry_label.pack()
        self.__entry_box = Entry(top)
        self.__entry_box.pack()
        self.__checkbox_var = tkinter.IntVar()
        self.__check_button = Checkbutton(top, text="Unit in the csv file?", variable=self.__checkbox_var)
        self.__check_button.pack()
        self.__submit_button = Button(top, text='Submit', command=self.submit)
        self.__submit_button.pack()
        self.__input_options = {
            'delimiter': ';',
            'unit': 1
        }

    def submit(self):
        """ submit_button action to submit entry options and destroy the frame """
        if self.__entry_box.get():
            self.__input_options['delimiter'] = self.__entry_box.get()
        self.__input_options['unit'] = self.__checkbox_var.get()
        self.top.destroy()
        logger.log(logging.DEBUG, "[InputDialog] " + str(self.__input_options))

    def get_input_options(self):
        """ Get entry options """
        return self.__input_options
