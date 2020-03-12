#!/usr/bin/python
# coding: utf-8

""" This file contains the CsvFrame class """

import tkinter
from tkinter.ttk import Frame, Scrollbar, Treeview


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
    quit()
        destroy the frame
    """

    def __init__(self, parent, manager):
        """ CsvFrame constructor """
        top = self.top = tkinter.Toplevel(parent)

        table = Frame(top)
        table.pack(expand=True, fill=tkinter.BOTH)
        scrollbar_x = Scrollbar(table, orient=tkinter.HORIZONTAL)
        scrollbar_y = Scrollbar(table, orient=tkinter.VERTICAL)
        tree = Treeview(table, columns=manager.get_field_names(), show="headings", selectmode="extended",
                        yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.config(command=tree.yview)
        scrollbar_y.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scrollbar_x.config(command=tree.xview)
        scrollbar_x.pack(side=tkinter.BOTTOM, fill=tkinter.X)

        for field_name in manager.get_field_names():
            tree.heading(field_name, text=field_name, anchor=tkinter.W)
            tree.column(field_name, stretch=tkinter.YES)

        for entry in manager.get_data_tuple():
            tree.insert("", 'end', values=entry)
        tree.pack(expand=True, fill=tkinter.BOTH)

    def quit(self):
        """ Destroy the frame """
        self.top.destroy()
