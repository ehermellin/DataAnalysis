#!/usr/bin/python
# coding: utf-8

import tkinter
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Button

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from data import csvtools


class PlotFrame(tkinter.Frame):

    def __init__(self, parent, **kw):
        super().__init__(**kw)
        self.__parent = parent
        self.initialize()

    def initialize(self):
        # frame
        action_frame = tkinter.Frame(self, borderwidth=2, relief=tkinter.GROOVE)
        action_frame.pack(side=tkinter.TOP, fill=tkinter.X, padx=10, pady=10)

        list_frame = tkinter.Frame(self, borderwidth=2, relief=tkinter.GROOVE)
        list_frame.pack(side=tkinter.LEFT, fill=tkinter.Y, padx=10, pady=10)

        plot_frame = tkinter.Frame(self, borderwidth=2, relief=tkinter.GROOVE)
        plot_frame.pack(side=tkinter.RIGHT, padx=10, pady=10, fill=tkinter.BOTH, expand=True)

        # button
        load_button = Button(action_frame, text="Load data", command=self.load_data).grid(row=1, column=2, padx=5, pady=5)
        clear_button = Button(action_frame, text="Clear data", command=self.clear_data).grid(row=1, column=1, padx=5, pady=5)
        add_button = Button(action_frame, text="Add plot", command=self.add_plot).grid(row=1, column=5, padx=5, pady=5)

        remove_button = Button(list_frame, text="Remove plot")

        # list
        plot_list = tkinter.Listbox(list_frame)

        # combo
        data_list = ('Pomme', 'Poire', 'Banane')
        data_select_combo1 = tkinter.StringVar()
        variable1_combo = Combobox(action_frame, textvariable=data_select_combo1, values=data_list, state='readonly')\
            .grid(row=1, column=3, padx=5, pady=5)
        data_select_combo2 = tkinter.StringVar()
        variable2_combo = Combobox(action_frame, textvariable=data_select_combo2, values=data_list, state='readonly')\
            .grid(row=1, column=4, padx=5, pady=5)

        # pack
        plot_list.pack(padx=10, pady=10, fill=tkinter.Y, expand=1)
        remove_button.pack(padx=10, pady=10)

        # plot
        figure = Figure(figsize=(5, 5), dpi=100)
        figure.add_subplot(111)

        canvas = FigureCanvasTkAgg(figure, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(canvas, plot_frame)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def load_data(self):
        filename = askopenfilename(title="Open data file", filetypes=[('csv files', '.csv'), ('all files', '.*')])
        if filename is not None and len(filename) > 0:
            reader = csvtools.read_csv_file(filename)
            for row in reader:
                print(row)

    def clear_data(self):
        pass

    def add_plot(self):
        pass
