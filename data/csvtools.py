#!/usr/bin/python
# coding: utf-8

import csv
from operator import itemgetter


def get_csv_field_names(reader):
    return reader.fieldnames


def get_data_from_field_names(csv_dictionary, field_name):
    return list(map(itemgetter(field_name), csv_dictionary))


class CsvTools:

    def __init__(self):
        self.__file = None

    def read_csv_file(self, filename):
        try:
            self.__file = open(filename, "r")
            reader = csv.DictReader(self.__file, delimiter=';')
            return reader
        except IOError:
            print("Oops!  Error when reading data file")

    def close_file(self):
        self.__file.close()

    def reset_file(self):
        self.__file = None
