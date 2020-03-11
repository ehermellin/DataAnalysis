#!/usr/bin/python
# coding: utf-8

""" This file contains the MainFrame class extending tkinter.Tk """

import logging
import tkinter
from tkinter.ttk import Notebook

from ranalysis.gui.loggerframe import LoggerFrame
from ranalysis.gui.plotframe import PlotFrame
from ranalysis.log.loghandler import logger


class MainFrame(tkinter.Tk):
    """ Main GUI window: Display menu and PlotFrame

    Attributes
    ----------
    parent : tkinter.Frame
        the parent frame of the MainFrame

    Methods
    -------
    initialize()
        initialize all the tkinter objects of the frame
    add_tab_command(self)
        add_tab_command action of the menu creating new notebook tab
    remove_tab_command(self)
        remove_tab_command action of the menu removing selected notebook tab
    logger(self)
        display or hide the LoggerFrame
    how_to_command(self)
        how_to_command action of the menu displaying some "how to" questions
    about_command(self)
       about_command action of the menu displaying RAnalysis informations
    """

    def __init__(self, parent):
        """ MainFrame constructor """
        tkinter.Tk.__init__(self, parent)
        self.__parent = parent
        self.__notebook = Notebook(self)
        self.__logger_frame = None
        self.__counter = 0
        self.initialize()

    def initialize(self):
        """ Initialize all the tkinter objects of the frame """
        self.title('RGINE Data Analysis')

        # notebook
        self.__notebook.pack(expand=1, fill='both')

        # menu
        frame_menu = tkinter.Menu(self)

        options_menu = tkinter.Menu(frame_menu, tearoff=0)
        options_menu.add_command(label="Add tab", command=self.add_tab_command)
        options_menu.add_command(label="Remove tab", command=self.remove_tab_command)
        frame_menu.add_cascade(label="Tabs", menu=options_menu)

        help_menu = tkinter.Menu(frame_menu, tearoff=0)
        help_menu.add_command(label="Logger", command=self.logger)
        help_menu.add_separator()
        help_menu.add_command(label="How to", command=self.how_to_command)
        help_menu.add_command(label="About", command=self.about_command)
        frame_menu.add_cascade(label="Help", menu=help_menu)

        self.config(menu=frame_menu)
        self.add_tab_command()

    def add_tab_command(self):
        """ add_tab_command action of the menu creating new notebook tab """
        self.__counter += 1
        tab = PlotFrame(self)
        self.__notebook.add(tab, text="Plot frame " + str(self.__counter))
        logger.log(logging.INFO, "[MainFrame] Add tab: " + str(self.__counter))

    def remove_tab_command(self):
        """ remove_tab_command action of the menu removing selected notebook tab """
        self.__notebook.forget(self.__notebook.select())
        logger.log(logging.INFO, "[MainFrame] Remove tab")

    def logger(self):
        """ Display or hide the LoggerFrame """
        logger.log(logging.INFO, "[MainFrame] Open Logger frame")
        if self.__logger_frame is not None:
            self.__logger_frame.quit()
        self.__logger_frame = None
        self.__logger_frame = LoggerFrame(self)

    def how_to_command(self):
        """ how_to_command action of the menu displaying some "how to" questions """
        pass

    def about_command(self):
        """ about_command action of the menu displaying RAnalysis informations """
        pass

