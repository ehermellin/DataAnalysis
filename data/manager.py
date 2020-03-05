#!/usr/bin/python
# coding: utf-8

import csv


class DataManager:

    def __init__(self):
        self.__fieldnames = []
        self.__data = {}
        self.__unit_in_data = 1

    def read_csv_file(self, filename, options):
        self.__unit_in_data = options['unit']
        with open(filename, 'rU') as infile:
            # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile, delimiter=options['delimiter'])
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

    def get_unit_from_field_name(self, field_name):
        if self.__unit_in_data == 1:
            return self.__data[field_name][0]
        else:
            return ""

    def get_data_from_field_name(self, field_name):
        return self.copy_and_adapt_data(self.__data[field_name])

    def reset_manager(self):
        self.__fieldnames = ()
        self.__data = {}
        self.__unit_in_data = 1

    def copy_and_adapt_data(self, data):
        data_temp = data.copy()
        if self.__unit_in_data == 1:
            data_temp.remove(data_temp[0])
        data_temp = [sub.replace(',', '.') for sub in data_temp]
        return list(map(float, data_temp))
