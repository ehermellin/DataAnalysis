#!/usr/bin/python
# coding: utf-8

import logging

logger = logging.getLogger(__name__)


class QueueHandler(logging.Handler):
    """Class to send logging records to a queue
    It can be used from different threads
    """

    def __init__(self, log_queue):
        super().__init__()
        self.log_queue = log_queue

    def emit(self, record):
        self.log_queue.put(record)
