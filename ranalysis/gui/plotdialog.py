#!/usr/bin/python
# coding: utf-8

""" This file contains the PlotDialog class """

import logging
import tkinter
from tkinter.ttk import Checkbutton, Button, Entry, Label

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from ranalysis.log.loghandler import logger
from ranalysis.plot.graph import graph_compare_plot, graph_clear, graph_compare_plot_diff, graph_compare_plot_values


class PlotDialog:
    """ Display plot dialog for plotting multiple plot

    Attributes
    ----------
    parent : tkinter.Frame
        the parent frame of the PlotDialog
    """

    def __init__(self, parent, plot1, plot2, marker="."):
        """ PlotDialog constructor """
        self.__plots = [plot1, plot2]
        self.__marker = marker

        top = self.top = tkinter.Toplevel(parent)
        logger.log(logging.DEBUG, "[PlotDialog] Comparing two plots " + plot1.get_name() + " " + plot2.get_name())

        top_frame = tkinter.Frame(top, borderwidth=2, relief=tkinter.GROOVE)
        top_frame.pack(side=tkinter.TOP, fill=tkinter.X, padx=10, pady=10)

        self.__chkbx_g = tkinter.IntVar()
        self.__chkbx_g.set(1)
        self.__check_graph = Checkbutton(top_frame, text="Display graphs to compare", variable=self.__chkbx_g)
        self.__check_graph.grid(row=1, column=1, rowspan=1, padx=5, pady=5)
        self.__chkbx_d = tkinter.IntVar()
        self.__check_graph_diff = Checkbutton(top_frame, text="Display diff as graph", variable=self.__chkbx_d)
        self.__check_graph_diff.grid(row=1, column=2, rowspan=1, padx=5, pady=5)
        self.__chkbx_v = tkinter.IntVar()
        self.__check_graph_values = Checkbutton(top_frame, text="Display diff as values", variable=self.__chkbx_v)
        self.__check_graph_values.grid(row=2, column=2, rowspan=1, padx=5, pady=5)

        label_threshold = Label(top_frame, text="Diff threshold:", anchor="w")
        label_threshold.grid(row=1, column=3, padx=5, pady=5)
        self.__entry_threshold = Entry(top_frame, width=15)
        self.__entry_threshold.insert(tkinter.END, '0.1')
        self.__entry_threshold.grid(row=1, column=4, columnspan=1, rowspan=1, padx=5, pady=5)

        label_round = Label(top_frame, text="Diff round:", anchor="w")
        label_round.grid(row=2, column=3, padx=5, pady=5)
        self.__entry_round = Entry(top_frame, width=15)
        self.__entry_round.insert(tkinter.END, '2')
        self.__entry_round.grid(row=2, column=4, columnspan=1, rowspan=1, padx=5, pady=5)

        display_button = Button(top_frame, text="Display", command=self.display, width=15)
        display_button.grid(row=1, column=5, rowspan=1, padx=5, pady=5)

        clear_button = Button(top_frame, text="Clear", command=self.clear, width=15)
        clear_button.grid(row=2, column=5, rowspan=1, padx=5, pady=5)

        graph_frame = tkinter.Frame(top, borderwidth=2, relief=tkinter.GROOVE)
        graph_frame.pack(side=tkinter.BOTTOM, padx=10, pady=10, fill=tkinter.BOTH, expand=True)
        figure = Figure(figsize=(8, 4))
        self.__graph = figure.add_subplot(111)

        self.__canvas = FigureCanvasTkAgg(figure, master=graph_frame)
        self.__canvas.draw()
        self.__canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.__canvas, graph_frame)
        toolbar.update()
        self.__canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        graph_compare_plot(self.__graph, plot1, plot2, self.__marker)
        self.__canvas.draw()

    def display(self):
        """ Display in the graph frame """
        graph_clear(self.__graph)

        if self.__chkbx_g.get():
            graph_compare_plot(self.__graph, self.__plots[0], self.__plots[1], self.__marker)

        if self.__chkbx_d.get():
            graph_compare_plot_diff(self.__graph, self.__plots[0], self.__plots[1], self.__marker)

        if self.__chkbx_v.get():
            graph_compare_plot_values(self.__graph, self.__plots[0], self.__plots[1],
                                      float(self.__entry_threshold.get()), bool(self.__chkbx_d.get()),
                                      int(self.__entry_round.get()))
        self.__canvas.draw()

    def clear(self):
        """ Clear the graph frame """
        graph_clear(self.__graph)
        self.__canvas.draw()
