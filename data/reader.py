#!/usr/bin/python
# coding: utf-8

import csv


class Reader:

    def __init__(self):
        self.__fieldnames = []
        self.__data = {}

    def read_csv_file(self, filename, delimiter):
        if len(delimiter) == 0:
            delimiter = ";"

        with open(filename, 'rU') as infile:
            # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile, delimiter=delimiter)
            for row in reader:
                for header, value in row.items():
                    try:
                        self.__data[header].append(value)
                        if header not in self.__fieldnames:
                            self.__fieldnames.append(header)
                    except KeyError:
                        self.__data[header] = [value]

    def get_field_names(self):
        return self.__fieldnames

    def get_data_from_field_name(self, field_name):
        return self.__data[field_name]

    def reset_reader(self):
        self.__fieldnames = ()
        self.__data = {}
