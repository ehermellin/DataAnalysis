#!/usr/bin/python
# coding: utf-8

import tkinter
from tkinter.ttk import Notebook

from gui.plot import PlotFrame


class MainFrame(tkinter.Tk):
    def __init__(self,parent):
        tkinter.Tk.__init__(self,parent)
        self.__parent = parent
        self.__notebook = Notebook(self)
        self.__counter = 0
        self.initialize()

    def initialize(self):
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
        help_menu.add_command(label="How to", command=self.how_to_command)
        help_menu.add_command(label="About", command=self.about_command)
        frame_menu.add_cascade(label="Help", menu=help_menu)

        self.config(menu=frame_menu)
        self.add_tab_command()

    def add_tab_command(self):
        self.__counter += 1
        tab = PlotFrame(self)
        self.__notebook.add(tab, text="Plot frame " + str(self.__counter))

    def remove_tab_command(self):
        self.__notebook.forget(self.__notebook.select())

    def how_to_command(self):
        pass

    def about_command(self):
        pass

