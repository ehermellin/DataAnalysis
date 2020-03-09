#!/usr/bin/python
# coding: utf-8

import argparse

from gui.mainframe import MainFrame

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-gui', action='store_true',
                        help='run ranalysis with gui')
    parser.add_argument('-f', action='store', type=str,
                        help='the absolute path to the csv (data) file')
    parser.add_argument('-x', action='store', type=str,
                        help='the field name of the x data (from csv file)')
    parser.add_argument('-y', action='store', type=str,
                        help='the field name of the y data (from csv file)')
    args = parser.parse_args()

    if args.gui:
        parser.print_usage()
        app = MainFrame(None)
        app.mainloop()
    else:
        if args.f:
            parser.print_usage()
            pass
        else:
            parser.print_help()
