#!/usr/bin/python
# coding: utf-8

import logging

from gui.mainframe import MainFrame
from log.handler import logger

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.log(logging.INFO, "[Main] Starting RAnalysis")
    app = MainFrame(None)
    app.mainloop()
