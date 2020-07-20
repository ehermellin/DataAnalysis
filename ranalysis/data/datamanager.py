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
        __filename : str
            the path to the data file
        __reading_options : dict
            the reding options of the csv file
        __fieldnames : list(str)
            list of fieldnames (name of the data variables)
        __data_unit : list(str)
            list of data unit
        __data : dict
            the read csv data

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
        refresh_data()
            refresh the data
        clear_data()
            clear the data
        reset_manager()
            reset the data manager
        __copy_and_adapt_data(data)
            correct and return a list of data
        """

    def __init__(self):
        """ DataManager constructor """
        self.__filename = ""
        self.__reading_options = {}

        self.__fieldnames = []
        self.__data_unit = []
        self.__data = {}
        self.__data_values_as_list_tuple = []

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
        self.__filename = filename
        self.__reading_options = options
        logger.log(logging.DEBUG, "[DataManager] " + self.__filename + " " + str(self.__reading_options))

        if self.__reading_options['clear']:
            self.clear_data()

        counter = 0
        with open(self.__filename, 'rU') as infile:
            # read the file as a dictionary for each row ({header : value})
            reader = csv.DictReader(infile, delimiter=self.__reading_options['delimiter'])
            for row in reader:
                for header, value in row.items():
                    if header not in self.__fieldnames:
                        self.__fieldnames.append(header)

                    if self.__reading_options['unit'] == 1 and counter == 0:
                        self.__data_unit.insert(self.__fieldnames.index(header), value)

                    else:
                        try:
                            value_temp = float(value.replace(',', '.'))
                            try:
                                self.__data[header].append(value_temp)
                            except KeyError:
                                logger.log(logging.DEBUG, "[DataManager] Key error:" + header + " " + value)
                                self.__data[header] = [value]
                        except ValueError:
                            print("test")

                counter += 1

        self.dict_to_list_tuple()

    def add_data(self):
        # TODO faire l'ajout de données dans la structure du DataManager !!
        pass

    def dict_to_list_tuple(self):
        """ Convert dictionary values into list of tuple """

        # TODO Peut être reset cette variable avant !!!!!!
        self.__data_values_as_list_tuple = []
        dict_values_to_list = list(self.__data.values())

        print(dict_values_to_list)

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
        if field_name in self.__fieldnames:
            if self.__reading_options['unit'] == 1:
                return self.__data_unit[self.__fieldnames.index(field_name)]
            else:
                return ""
        else:
            logger.log(logging.ERROR, "[DataManager] Error field name does not exist (get unit)")
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
            return copy_and_adapt_data(self.__data[field_name])
        else:
            logger.log(logging.ERROR, "[DataManager] Error field name does not exist (get data)")
            return list()

    def clear_data(self):
        """ Clear data """
        logger.log(logging.DEBUG, "[DataManager] Clear data")
        self.__fieldnames = []
        self.__data = {}
        self.__data_values_as_list_tuple = []

    def refresh_data(self):
        """ Refresh data from the same data file """
        if self.__filename != "":
            logger.log(logging.DEBUG, "[DataManager] Refresh data")
            self.clear_data()
            self.read_csv_file(self.__filename, self.__reading_options)
        else:
            logger.log(logging.DEBUG, "[DataManager] Cannot refresh data because no data file is defined")

    def reset_manager(self):
        """ Reset the data manager """
        logger.log(logging.DEBUG, "[DataManager] Reset data manager")
        self.__filename = ""
        self.__reading_options = {}
        self.__fieldnames = []
        self.__data = {}
        self.__data_values_as_list_tuple = []


def copy_and_adapt_data(data):
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
    try:
        data_temp = list(map(float, data_temp))
        return data_temp
    except ValueError:
        logger.log(logging.ERROR, "[DataManager] Error when converting data (string to number)")
        return list()
