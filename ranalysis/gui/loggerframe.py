#!/usr/bin/python
# coding: utf-8

""" This file contains the LoggerFrame class """

import logging
import queue
import tkinter
from tkinter import N, S, W, E
from tkinter.scrolledtext import ScrolledText

from ranalysis.log.loghandler import QueueHandler, logger


class LoggerFrame:
    """ Poll messages from a logging queue and display them in a scrolled text widget Attributes
    ----------
    parent : tkinter.Frame
        the parent frame of the LoggerFrame

    Methods
    -------
    display(record)
        display message in a scrolled text widget
    poll_log_queue()
        poll message from the queue and display it
    quit()
        destroy the frame
    """

    def __init__(self, parent):
        """ LoggerFrame constructor """
        top = self.top = tkinter.Toplevel(parent)

        # Create a ScrolledText wdiget
        self.__scrolled_text = ScrolledText(top, state='disabled', height=12)
        self.__scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.__scrolled_text.configure(font='TkFixedFont')
        self.__scrolled_text.tag_config('DEBUG', foreground='black')
        self.__scrolled_text.tag_config('DEBUG', foreground='gray')
        self.__scrolled_text.tag_config('WARNING', foreground='orange')
        self.__scrolled_text.tag_config('ERROR', foreground='red')
        self.__scrolled_text.tag_config('CRITICAL', foreground='red', underline=1)
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        self.queue_handler.setFormatter(logging.Formatter('%(asctime)s: %(message)s'))
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.top.after(100, self.poll_log_queue)

    def display(self, record):
        """ Display message in a scrolled text widget """
        msg = self.queue_handler.format(record)
        self.__scrolled_text.configure(state='normal')
        self.__scrolled_text.insert(tkinter.END, msg + '\n', record.levelname)
        self.__scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.__scrolled_text.yview(tkinter.END)

    def poll_log_queue(self):
        """ Poll message from the queue and display it """
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.top.after(100, self.poll_log_queue)

    def quit(self):
        """ Destroy the frame """
        self.top.destroy()
