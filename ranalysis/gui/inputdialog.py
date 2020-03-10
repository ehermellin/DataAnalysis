#!/usr/bin/python
# coding: utf-8

import logging
import tkinter
from tkinter.ttk import Label, Entry, Checkbutton, Button

from ranalysis.log.loghandler import logger


class InputDialog:

    def __init__(self, parent):
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
        if self.__entry_box.get():
            self.__input_options['delimiter'] = self.__entry_box.get()
        self.__input_options['unit'] = self.__checkbox_var.get()
        self.top.destroy()
        logger.log(logging.INFO, "[Input dialog] " + str(self.__input_options))

    def get_input_options(self):
        return self.__input_options
