#!/usr/bin/python
# coding: utf-8

import csv
from operator import itemgetter


def read_csv_file(filename):
    file = None
    try:
        file = open(filename, "rb")
        reader = csv.DictReader(file)
        return reader
    finally:
        file.close()


def get_csv_field_names(reader):
    return reader.fieldnames


def get_data_from_field_names(csv_dictionary, field_name):
    return list(map(itemgetter(field_name), csv_dictionary))
