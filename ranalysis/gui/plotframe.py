#!/usr/bin/python
# coding: utf-8

""" This file contains the PlotFrame class extending tkinter.Frame """

import logging
import tkinter
from tkinter import simpledialog
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Button, Label

import matplotlib.pyplot as plt
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

from ranalysis.data.datamanager import DataManager
from ranalysis.gui.functiondialog import FunctionDialog
from ranalysis.gui.csvframe import CsvFrame
from ranalysis.gui.inputdialog import InputDialog
from ranalysis.gui.plotdialog import PlotDialog
from ranalysis.log.loghandler import logger
from ranalysis.plot.graph import graph_from_plot_ids, graph_clear, graph_add_title, graph_compare_plot
from ranalysis.plot.plotcreator import PlotCreator


class PlotFrame(tkinter.Frame):
    """ Display buttons, list, combobox and matplotlib canvas

    Attributes
    ----------
    parent : tkinter.Frame
        the parent frame of the PlotFrame

    Methods
    -------
    initialize()
        initialize all the tkinter objects of the frame
    create_plot(name_style='ggplot')
        create a matplotlib plot in a tkinter environment
    load_data()
        load_button action to load data from a csv file
    refresh_data()
        refresh data from the same csv file
    display_data()
        display csv data in a CsvFrame
    add_plot()
        add_button action to add created plot in the list
    customize_plot()
        customize_button action to change the matplotlib plot style
    remove_plot()
        remove_button action to remove selected plot from the list
    compare_plot()
        compare two plots in a graph
    clear_plot()
        clear_button action to clear/reset the plot frame
    on_list_select(evt)
        display plots when plots are selected in the list (triggered by event on the list)
    add_title()
        add title to the matplotlib graph
    __reset_plotframe()
        reset plot frame attributes
    """

    def __init__(self, parent, **kw):
        """ PlotFrame constructor """
        super().__init__(**kw)
        self.__parent = parent
        self.__variable1_combo = None
        self.__variable2_combo = None
        self.__style_combo = None
        self.__plot_list = None
        self.__data_manager = DataManager()
        self.__canvas = None
        self.__graph = None
        self.__graph_frame = None
        self.compare_button = None
        self.csv_frame = None
        self.initialize()

    def initialize(self):
        """ Initialize all the tkinter objects """
        # frame
        top_frame = tkinter.Frame(self)
        top_frame.pack(side=tkinter.TOP, fill=tkinter.X)
        action_frame = tkinter.Frame(top_frame, borderwidth=2, relief=tkinter.GROOVE)
        action_frame.pack(side=tkinter.LEFT, fill=tkinter.X, padx=10, pady=10)
        customize_frame = tkinter.Frame(top_frame, borderwidth=2, relief=tkinter.GROOVE, width=100)
        customize_frame.pack(side=tkinter.RIGHT, fill=tkinter.X, padx=10, pady=10)

        list_frame = tkinter.Frame(self, borderwidth=2, relief=tkinter.GROOVE)
        list_frame.pack(side=tkinter.LEFT, fill=tkinter.Y, padx=10, pady=10)

        self.__graph_frame = tkinter.Frame(self, borderwidth=2, relief=tkinter.GROOVE)
        self.__graph_frame.pack(side=tkinter.RIGHT, padx=10, pady=10, fill=tkinter.BOTH, expand=True)

        # button
        load_button = Button(action_frame, text="Load data", command=self.load_data, width=35)
        load_button.grid(row=1, column=1, columnspan=2, rowspan=1, padx=5, pady=5)
        refresh_button = Button(action_frame, text="Refresh data", command=self.refresh_data, width=15)
        refresh_button.grid(row=2, column=1, padx=5, pady=5)
        display_button = Button(action_frame, text="Display data", command=self.display_data, width=15)
        display_button.grid(row=2, column=2, padx=5, pady=5)
        add_button = Button(action_frame, text="Add plot", command=self.add_plot, width=15)
        add_button.grid(row=1, column=5, rowspan=1, padx=5, pady=5)
        title_button = Button(action_frame, text="Add title", command=self.add_title, width=15)
        title_button.grid(row=2, column=5, rowspan=1, padx=5, pady=5)

        customize_button = Button(customize_frame, text="Customize plot", command=self.customize_plot, width=35)
        customize_button.grid(row=2, column=1, columnspan=2, rowspan=1, padx=5, pady=5)

        function_button = Button(action_frame, text="Plot math function", command=self.add_plot_function, width=35)
        function_button.grid(row=1, column=7, columnspan=2, rowspan=1, padx=5, pady=5)
        clear_button = Button(action_frame, text="Clear all plots", command=self.clear_plot, width=35)
        clear_button.grid(row=2, column=7, columnspan=2, rowspan=1, padx=5, pady=5)

        remove_button = Button(list_frame, text="Remove plot", command=self.remove_plot, width=20)
        self.compare_button = Button(list_frame, state=tkinter.DISABLED, text="Compare two plots",
                                     command=self.compare_plots, width=20)

        # label
        label_x = Label(action_frame, text="Choose x axis: ")
        label_x.grid(row=1, column=3, padx=5, pady=5)
        label_y = Label(action_frame, text="Choose y axis: ")
        label_y.grid(row=2, column=3, padx=5, pady=5)
        label_style = Label(customize_frame, text="Choose style: ")
        label_style.grid(row=1, column=1, rowspan=1, padx=5, pady=5)

        # list
        self.__plot_list = tkinter.Listbox(list_frame, selectmode=tkinter.MULTIPLE, exportselection=False)
        self.__plot_list.bind('<<ListboxSelect>>', self.on_list_select)

        # combo
        data_select_combo1 = tkinter.StringVar()
        self.__variable1_combo = Combobox(action_frame, textvariable=data_select_combo1,
                                          values=self.__data_manager.get_field_names(),
                                          state='readonly',
                                          postcommand=lambda: self.__variable1_combo
                                          .configure(values=self.__data_manager.get_field_names()))
        self.__variable1_combo.grid(row=1, column=4, padx=5, pady=5)
        data_select_combo2 = tkinter.StringVar()
        self.__variable2_combo = Combobox(action_frame, textvariable=data_select_combo2,
                                          values=self.__data_manager.get_field_names(),
                                          state='readonly',
                                          postcommand=lambda: self.__variable2_combo
                                          .configure(values=self.__data_manager.get_field_names()))
        self.__variable2_combo.grid(row=2, column=4, padx=5, pady=5)
        style_select_combo3 = tkinter.StringVar()
        self.__style_combo = Combobox(customize_frame, textvariable=style_select_combo3, values=style.available,
                                      state='readonly')
        self.__style_combo.grid(row=1, column=2, rowspan=1, padx=5, pady=5)

        # pack
        self.__plot_list.pack(padx=10, pady=10, fill=tkinter.Y, expand=1)
        remove_button.pack(padx=10, pady=5)
        self.compare_button.pack(padx=10, pady=5)

        # plot
        self.create_plot()

    def add_plot_function(self):
        """ Create plot from math functions to validate data """
        compare_dialog = FunctionDialog(self)
        self.wait_window(compare_dialog.top)
        if compare_dialog.get_plot() is not None:
            self.__plot_list.insert(tkinter.END, compare_dialog.get_plot())

    def create_plot(self, name_style='ggplot'):
        """ Create a matplotlib plot in a tkinter environment """
        if self.__canvas is not None:
            self.__canvas.get_tk_widget().destroy()
        if self.__graph_frame is not None:
            self.__graph_frame.destroy()

        self.__graph = None
        self.__canvas = None
        self.__graph_frame = None

        self.__graph_frame = tkinter.Frame(self, borderwidth=2, relief=tkinter.GROOVE)
        self.__graph_frame.pack(side=tkinter.RIGHT, padx=10, pady=10, fill=tkinter.BOTH, expand=True)

        style.use(name_style)
        figure = Figure(figsize=(5, 5))
        self.__graph = figure.add_subplot(111)
        figure.subplots_adjust(left=0.06)

        self.__canvas = FigureCanvasTkAgg(figure, master=self.__graph_frame)
        self.__canvas.draw()
        self.__canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.__canvas, self.__graph_frame)
        toolbar.update()
        self.__canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def load_data(self):
        """ Load data from a csv file """

        filename = askopenfilename(title="Open data file", filetypes=[('csv files', '.csv'), ('all files', '.*')])

        if filename is not None and len(filename) > 0:
            self.__reset_plotframe()

            if self.__data_manager is not None:
                self.__data_manager.reset_manager()
            else:
                self.__data_manager = DataManager()

            input_dialog = InputDialog(self)
            self.wait_window(input_dialog.top)
            logger.log(logging.DEBUG, "[PlotFrame] Open file:" + str(filename))
            self.__data_manager.read_csv_file(filename, input_dialog.get_input_options())
        else:
            logger.log(logging.ERROR, "[PlotFrame] No file selected")

    def refresh_data(self):
        """ Refresh data from the same csv file """
        if self.__data_manager.manager_have_data():
            self.__data_manager.refresh_data()
            PlotCreator.get_instance().refresh_plots(self.__data_manager)
            self.on_list_select(None)
            if self.csv_frame is not None:
                self.csv_frame.fill_data()

    def display_data(self):
        """ Display csv data in a CsvFrame """
        if self.__data_manager.manager_have_data():
            self.csv_frame = CsvFrame(self, self.__data_manager, self.__canvas, self.__graph)

    def add_plot(self):
        """ Add_button action to add created plot in the list """
        if self.__variable1_combo.get() != "" and self.__variable2_combo.get() != "":
            if self.__data_manager.manager_have_data():
                plot_f = PlotCreator.get_instance()
                plot = plot_f.plot_from_fieldnames(self.__data_manager, self.__variable1_combo.get(),
                                                   [self.__variable2_combo.get()])
                logger.log(logging.DEBUG, "[PlotFrame] Add plot: " + str(plot[0]))
                self.__plot_list.insert(tkinter.END, plot[0])
                self.__variable1_combo["state"] = 'disabled'
            else:
                logger.log(logging.ERROR, "[PlotFrame] Data manager does not have data")
        else:
            logger.log(logging.ERROR, "[PlotFrame] No variables selected")

    def customize_plot(self):
        """ Change the matplotlib plot style """
        if self.__style_combo.get() != "":
            logger.log(logging.DEBUG, "[PlotFrame] Style: " + self.__style_combo.get())
            self.create_plot(self.__style_combo.get())

    def remove_plot(self):
        """ Remove selected plot from the list """
        if self.__plot_list.size() > 0:
            logger.log(logging.DEBUG, "[PlotFrame] Remove plot")
            idxs = self.__plot_list.curselection()
            for idx in idxs:
                self.__plot_list.delete(idx)
        else:
            logger.log(logging.ERROR, "[PlotFrame] No plot to remove")

        if self.__plot_list.size() == 0:
            self.__variable1_combo["state"] = 'readonly'

    def compare_plots(self):
        """ Compare two plots in a graph """
        plot_ids = []
        for idx in self.__plot_list.curselection():
            plot_ids.append(self.__plot_list.get(idx))

        PlotDialog(self, PlotCreator.get_instance().get_plot_from_stringify(plot_ids[0]),
                   PlotCreator.get_instance().get_plot_from_stringify(plot_ids[1]))

    def clear_plot(self):
        """ Clear/reset the plot frame """
        logger.log(logging.DEBUG, "[PlotFrame] Clear all plots")
        graph_clear(self.__graph)
        self.__plot_list.selection_clear(0, tkinter.END)
        self.__canvas.draw()

    def on_list_select(self, evt):
        """ Display plots when plots are selected in the list (triggered by event on the list) """
        plot_ids = []
        for idx in self.__plot_list.curselection():
            plot_ids.append(self.__plot_list.get(idx))

        if len(self.__plot_list.curselection()) == 2:
            self.compare_button['state'] = 'normal'
        else:
            self.compare_button['state'] = 'disabled'

        if len(plot_ids) > 0:
            graph_from_plot_ids(self.__graph, plot_ids)
            self.__canvas.draw()
        else:
            self.clear_plot()

    def add_title(self):
        """ Add title to the graph"""
        title = simpledialog.askstring("Graph Title", "What is the title of the Graph?", parent=self)
        if title is not None and title != "":
            graph_add_title(self.__graph, title)
            self.__canvas.draw()

    def reset_csvframe(self):
        """ Reset csv frame """
        self.csv_frame = None

    def __reset_plotframe(self):
        """ Reset plot frame attributes """
        self.__variable1_combo.set('')
        self.__variable2_combo.set('')
        self.__plot_list.delete(0, tkinter.END)
        self.__variable1_combo["state"] = 'readonly'
