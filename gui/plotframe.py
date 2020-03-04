#!/usr/bin/python
# coding: utf-8

import tkinter
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Button, Checkbutton

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure

from data.manager import DataManager
from plot.plotfactory import PlotFactory


class PlotFrame(tkinter.Frame):

    def __init__(self, parent, **kw):
        super().__init__(**kw)
        self.__parent = parent
        self.__data_field_names = []
        self.__entree = None
        self.__variable1_combo = None
        self.__variable2_combo = None
        self.__plot_list = None
        self.__data_manager = DataManager()
        self.__canvas = None
        self.__plot = None
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
        load_button = Button(action_frame, text="Load data", command=self.load_data)
        load_button.grid(row=1, column=1, padx=5, pady=5)
        add_button = Button(action_frame, text="Add plot", command=self.add_plot)
        add_button.grid(row=1, column=6, padx=5, pady=5)
        remove_button = Button(list_frame, text="Remove plot", command=self.remove_plot)

        # list
        self.__plot_list = tkinter.Listbox(list_frame, selectmode=tkinter.MULTIPLE)
        self.__plot_list.bind('<<ListboxSelect>>', self.on_list_select)

        # combo
        data_select_combo1 = tkinter.StringVar()
        self.__variable1_combo = Combobox(action_frame, textvariable=data_select_combo1, values=self.__data_field_names,
                                          state='readonly',
                                          postcommand=lambda: self.__variable1_combo.configure(values=
                                                                                               self.__data_field_names))
        self.__variable1_combo.grid(row=1, column=4, padx=5, pady=5)
        data_select_combo2 = tkinter.StringVar()
        self.__variable2_combo = Combobox(action_frame, textvariable=data_select_combo2, values=self.__data_field_names,
                                          state='readonly',
                                          postcommand=lambda: self.__variable2_combo.configure(values=
                                                                                               self.__data_field_names))
        self.__variable2_combo.grid(row=1, column=5, padx=5, pady=5)

        # pack
        self.__plot_list.pack(padx=10, pady=10, fill=tkinter.Y, expand=1)
        remove_button.pack(padx=10, pady=10)

        # plot
        figure = Figure(figsize=(5, 5))
        self.__plot = figure.add_subplot(111)

        self.__canvas = FigureCanvasTkAgg(figure, master=plot_frame)
        self.__canvas.draw()
        self.__canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.__canvas, plot_frame)
        toolbar.update()
        self.__canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    def load_data(self):
        self.__variable1_combo.set('')
        self.__variable2_combo.set('')
        self.__data_field_names = []
        self.__data_manager = DataManager()
        filename = askopenfilename(title="Open data file", filetypes=[('csv files', '.csv'), ('all files', '.*')])
        if filename is not None and len(filename) > 0:
            self.__data_manager.read_csv_file(filename, self.__entree.get())
            self.__data_field_names = self.__data_manager.get_field_names()

    def add_plot(self):
        if self.__variable1_combo.get() != "" and self.__variable2_combo.get() != "":
            plot_f = PlotFactory.get_instance()
            plot = plot_f.plot_from_data(self.__data_manager.get_data_from_field_name(self.__variable1_combo.get()),
                                         self.__data_manager.get_data_from_field_name(self.__variable2_combo.get()),
                                         self.__variable1_combo.get(), self.__variable2_combo.get())

            self.__plot_list.insert(tkinter.END, plot)

    def remove_plot(self):
        input_dialog = InputDialog(self)
        self.wait_window(inputDialog.top)
        print('Username: ', inputDialog.username)

        if self.__plot_list.size() > 0:
            idxs = self.__plot_list.curselection()
            for idx in idxs:
                self.__plot_list.delete(idx)

    def on_list_select(self, evt):
        plot_f = PlotFactory.get_instance()
        plot_ids = []
        widget_list = evt.widget
        for idx in widget_list.curselection():
            plot_ids.append(widget_list.get(idx))
        plot_f.matplotlib_from_plot(self.__plot, plot_ids, {})
        self.__canvas.draw()


class InputDialog:

    def __init__(self, parent):
        top = self.top = tkinter.Toplevel(parent)
        self.myLabel = tkinter.Label(top, text='Enter the delimiter of the csv file:')
        self.myLabel.pack()
        self.myEntryBox = tkinter.Entry(top)
        self.myEntryBox.pack()
        self.check_button = Checkbutton(top, text="Unit in the csv file?")
        self.check_button.pack()
        self.mySubmitButton = tkinter.Button(top, text='Submit', command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        #input = {}
        #input['delimiter'] =
        #input['unit'] =
        self.username = self.myEntryBox.get()
        self.top.destroy()
