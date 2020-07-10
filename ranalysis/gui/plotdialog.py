#!/usr/bin/python
# coding: utf-8

""" This file contains the PlotDialog class """

import logging
import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from ranalysis.log.loghandler import logger
from ranalysis.plot.graph import graph_compare_plot


class PlotDialog:
    """ Display plot dialog for plotting multiple plot

    Attributes
    ----------
    parent : tkinter.Frame
        the parent frame of the PlotDialog
    """

    def __init__(self, parent, plot1, plot2):
        """ PlotDialog constructor """
        top = self.top = tkinter.Toplevel(parent)
        logger.log(logging.DEBUG, "[PlotDialog] Comparing two plots " + plot1.get_name() + " " + plot2.get_name())
        graph_frame = tkinter.Frame(top, borderwidth=2, relief=tkinter.GROOVE)
        graph_frame.pack(side=tkinter.TOP, padx=10, pady=10, fill=tkinter.BOTH, expand=True)
        figure = Figure(figsize=(8, 4))
        graph = figure.add_subplot(111)

        canvas = FigureCanvasTkAgg(figure, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, graph_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        graph_compare_plot(graph, plot1, plot2)
        canvas.draw()
