#!/usr/bin/python
# coding: utf-8

""" This file contains the CsvFrame class """

import tkinter
from tkinter.ttk import Frame, Scrollbar, Treeview, Combobox, Label


class CsvFrame:
    """ Display csv data in a tkinter TreeView

    Attributes
    ----------
    parent : tkinter.Frame
        the parent frame of the LoggerFrame
    manager : DataManager
        the data manager

    Methods
    -------
    on_tree_select(event)
        action when item in tree is selected
    quit()
        destroy the frame
    """

    def __init__(self, parent, manager, canvas=None, graph=None):
        """ CsvFrame constructor """
        top = self.top = tkinter.Toplevel(parent)
        self.__parent = parent
        self.__manager = manager
        self.__associated_canvas = canvas
        self.__associated_graph = graph

        action_frame = tkinter.Frame(top, borderwidth=2, relief=tkinter.GROOVE)
        action_frame.pack(side=tkinter.TOP, fill=tkinter.X, padx=10, pady=10)
        label_x = Label(action_frame, text="Choose x axis: ")
        label_x.grid(row=1, column=1, padx=5, pady=5)
        data_select_combo1 = tkinter.StringVar()
        self.combo_x = Combobox(action_frame, textvariable=data_select_combo1, values=manager.get_field_names(),
                                state='readonly',
                                postcommand=lambda: self.combo_x.configure(values=manager.get_field_names()))
        self.combo_x.grid(row=1, column=2, padx=5, pady=5)
        label_y = Label(action_frame, text="Choose y axis: ")
        label_y.grid(row=1, column=3, padx=5, pady=5)
        data_select_combo2 = tkinter.StringVar()
        self.combo_y = Combobox(action_frame, textvariable=data_select_combo2, values=manager.get_field_names(),
                                state='readonly',
                                postcommand=lambda: self.combo_y.configure(values=manager.get_field_names()))
        self.combo_y.grid(row=1, column=4, padx=5, pady=5)

        table_frame = Frame(top)
        table_frame.pack(side=tkinter.BOTTOM, expand=True, fill=tkinter.BOTH)
        scrollbar_x = Scrollbar(table_frame, orient=tkinter.HORIZONTAL)
        scrollbar_y = Scrollbar(table_frame, orient=tkinter.VERTICAL)
        self.tree = Treeview(table_frame, columns=manager.get_field_names(), show="headings", selectmode="extended",
                             yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        scrollbar_y.config(command=self.tree.yview)
        scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollbar_x.config(command=self.tree.xview)
        scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        for field_name in manager.get_field_names():
            self.tree.heading(field_name, text=field_name, anchor=tkinter.W)
            self.tree.column(field_name, stretch=tkinter.YES)

        for entry in manager.get_data_tuple():
            self.tree.insert("", 'end', values=entry)
        self.tree.pack(expand=True, fill=tkinter.BOTH)

    def on_tree_select(self, event):
        list_values = self.tree.item(self.tree.selection())['values']
        if self.combo_x.get() != "" and self.combo_y.get() != "":
            index_x = self.__manager.get_field_names().index(self.combo_x.get())
            index_y = self.__manager.get_field_names().index(self.combo_y.get())
            if self.__associated_canvas is not None and self.__associated_graph is not None:
                value_x = list_values[index_x]
                if not isinstance(value_x, int):
                    value_x = value_x.replace(',', '.')

                value_y = list_values[index_y]
                if not isinstance(value_y, int):
                    value_y = value_y.replace(',', '.')

                self.__associated_graph.plot(float(value_x), float(value_y), marker='o', markersize=3, color="red")
                self.__associated_canvas.draw()

    def quit(self):
        """ Destroy the frame """
        self.top.destroy()
