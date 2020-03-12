#!/usr/bin/python
# coding: utf-8

""" This file contains the DataManager class """

import csv
import logging

from ranalysis.log.loghandler import logger


class DataManager:
    """ A class used to manage data from a csv file

        Attributes
        ----------
        __fieldnames : list(str)
            list of fieldnames (name of the data variables)
        __data : dict
            the read csv data
        __unit_in_data : int
            unit read from csv file (1 if units are in the file, 0 otherwise)

        Methods
        -------
        read_csv_file(filename, options)
            put the record in the log queue
        dict_to_list_tuple()
            convert dictionary values into list of tuple
        get_data_tuple()
            get the data as a list of tuple
        get_field_names()
            get list of data field names
        get_unit_from_field_name(field_name)
            get unit from data field name
        get_data_from_field_name(field_name)
            get data from data field name
        reset_manager()
            reset the data manager
        __copy_and_adapt_data(data)
            correct and return a list of data
        """

    def __init__(self):
        """ DataManager constructor """
        self.__fieldnames = []

        self.__data = {}
        self.__data_values_as_list_tuple = []

        self.__unit_in_data = 1

    def manager_have_data(self):
        """ Does the manager contains data read from csv file ?

        Returns
        ------
        bool
            true if manager has data, false otherwise
        """
        return bool(self.__data)

    def read_csv_file(self, filename, options):
        """ Read a csv file from its file name and options and fill data in dictionary

        Parameters
        ----------
        filename : str
            the file name of the csv file
        options : dict
            the reading options of the csv file
        """
        self.__unit_in_data = options['unit']
        logger.log(logging.DEBUG, "[DataManager] " + filename + " " + str(options))
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
                        logger.log(logging.DEBUG, "[DataManager] Key error:" + header + " " + value)
                        self.__data[header] = [value]
        self.dict_to_list_tuple()

    def dict_to_list_tuple(self):
        """ Convert dictionary values into list of tuple """
        dict_values_to_list = list(self.__data.values())

        # Test len of each list (must be equal)
        it = iter(dict_values_to_list)
        the_len = len(next(it))
        if not all(len(iter_list) == the_len for iter_list in it):
            logger.log(logging.ERROR, "[DataManager] Not all lists have same length")
        else:
            # Convert to tuple
            logger.log(logging.DEBUG, "[DataManager] Converting dict data to list of tuple")
            for i in range(the_len):
                temp_list = []
                for j in dict_values_to_list:
                    temp_list.append(j[i])
                self.__data_values_as_list_tuple.append(tuple(temp_list))

    def get_data_tuple(self):
        """ Get the data as a list of tuple

        Returns
        ------
        list(tuple)
            the data values as a list of tuple
        """
        return self.__data_values_as_list_tuple

    def get_field_names(self):
        """ Get the list of data field names

        Returns
        ------
        list(str)
            the list of data field names
        """
        return self.__fieldnames

    def get_unit_from_field_name(self, field_name):
        """ Get unit from data field name

        Parameters
        ----------
        field_name : str
            the data field name

        Returns
        ------
        str
            the unit of data field name
        """
        if field_name in self.__data:
            if self.__unit_in_data == 1:
                return self.__data[field_name][0]
            else:
                return ""
        else:
            logger.log(logging.ERROR, "[DataManager] Error field name does not exist")
            return ""

    def get_data_from_field_name(self, field_name):
        """ Get data from data field name

        Parameters
        ----------
        field_name : str
            the data field name

        Returns
        ------
        list(float, int, ...)
            the data of data field name
        """
        if field_name in self.__data:
            return self.__copy_and_adapt_data(self.__data[field_name])
        else:
            logger.log(logging.ERROR, "[DataManager] Error field name does not exist")
            return list()

    def reset_manager(self):
        """ Reset the data manager """
        logger.log(logging.DEBUG, "[DataManager] Reset data manager")
        self.__fieldnames = []
        self.__data = {}
        self.__data_values_as_list_tuple = []
        self.__unit_in_data = 1

    def __copy_and_adapt_data(self, data):
        """ Correct and return a list of data

        Parameters
        ----------
        data : list(float, int, ...)
            the list of data

        Returns
        ------
        list(float, int, ...)
            the copied and corrected data
        """
        data_temp = data.copy()
        if self.__unit_in_data == 1:
            data_temp.remove(data_temp[0])
        data_temp = [sub.replace(',', '.') for sub in data_temp]
        try:
            data_temp = list(map(float, data_temp))
            return data_temp
        except ValueError:
            logger.log(logging.ERROR, "[DataManager] Error when converting data (string to number)")
            return list()
