#!/usr/bin/python
# coding: utf-8

""" This file contains the QueueHandler class extending logging.Handler """

import logging

logger = logging.getLogger(__name__)


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue
    It can be used from different threads

    Attributes
    ----------
    log_queue : queue
        the queue

    Methods
    -------
    emit(record)
        put the record in the log queue
    """

    def __init__(self, log_queue):
        """ QueueHandler constructor

        Attributes
        ----------
        log_queue : queue
            the queue
        """
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        """ Emit a record (message) in the log queue

        Parameters
        ----------
        record : str
            the record (message) to put in the log queue
        """
        self.log_queue.put(record)
