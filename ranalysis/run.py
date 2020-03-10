#!/usr/bin/python
# coding: utf-8

import argparse
import logging

from ranalysis.cli.clihandler import CliHandler
from ranalysis.gui.mainframe import MainFrame
from ranalysis.log.loghandler import logger

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('-gui', action='store_true',
                        help='run ranalysis with gui')
    parser.add_argument('-f', action='store', type=str,
                        help='the absolute path to the csv data file')
    parser.add_argument('-x', action='store', type=str,
                        help='the field name of the x data from csv file ( -x xname )')
    parser.add_argument('-y', action='store', type=str,
                        help='the field name of the y data from csv file ( -y yname1 )')
    parser.add_argument('-my', action='store', type=str,
                        help='the field names of the y data from csv file ( -my yname1,yname2,yname3 ) ')
    args = parser.parse_args()

    if args.gui:
        logger.log(logging.INFO, "-- Running RAnalysis GUI version")
        parser.print_usage()
        app = MainFrame(None)
        app.mainloop()
    else:
        logger.log(logging.INFO, "-- Running RAnalysis CLI version")
        if args.f:
            if args.x:
                cli_handler = CliHandler(args.f)
                if args.y:
                    cli_handler.show_from_fieldname(args.x, args.y)
                elif args.my:
                    y_list = args.my.split(",")
                    cli_handler.show_from_fieldnames(args.x, y_list)
                else:
                    logger.log(logging.ERROR, "-- ERROR y data field name is missing")
            else:
                logger.log(logging.ERROR, "-- ERROR x data field name is missing")
        else:
            logger.log(logging.ERROR, "-- ERROR csv data file is missing")
            parser.print_help()
