#!/usr/bin/python
# coding: utf-8

""" This file contains the Plot class """


class Plot:
    """ A class used to represent a Plot

    A Plot is an object created from data and that will be used in matplotlib to be displayed

    Attributes
    ----------
    __plot_id : int
        the plot id (unique)
    __name : str
        the name of the plot
    __x :  list (int, float, ...)
        list of data (x-axis)
    __y : list (int, float, ...)
        list of data (y-axis)
    __x_axis : str
        the label of the x-axis ("")
    __y_axis : str
        the label of the y-axis ("")
    __x_unit : str
        the unit of the x-axis ("")
    __y_unit : str
        the unit of the x-axis ("")

    Methods
    -------
    get_plot_id()
        return the plot id (int)
    get_function()
        return function of the plot (str)
    set_function(function)
        set function of the plot
    use_function()
        return a boolean of the use of a function
    get_x()
        return x data (list)
    set_x(x_data)
        set x data
    set_y(y_data)
        set y data
    get_y()
        return y data (list)
    get_x_axis()
        return x axis label (str)
    get_y_axis()
        return y axis label (str)
    get_x_unit()
        return x unit label (str)
    get_y_unit()
        return y unit label (str)
    """

    def __init__(self, plot_id, x, y, x_axis="", y_axis="", x_unit="", y_unit=""):
        """ Plot constructor

        Parameters
        ----------
        plot_id : int
            the plot id (unique)
        x :  list (int, float, ...)
            list of data (x-axis)
        y : list (int, float, ...)
            list of data (y-axis)
        x_axis : str
            the label of the x-axis ("")
        y_axis : str
            the label of the y-axis ("")
        x_unit : str
            the unit of the x-axis ("")
        y_unit : str
            the unit of the x-axis ("")
        """
        self.__plot_id = plot_id
        self.__function = ""
        self.__x = x
        self.__y = y
        self.__x_axis = x_axis
        self.__y_axis = y_axis
        self.__x_unit = x_unit
        self.__y_unit = y_unit

    def __str__(self):
        """ Stringify plot object

        Returns
        ------
        str
            a stringify version of the plot
        """
        return "id=" + str(self.__plot_id) + " [" + self.__x_axis + " | " + self.__y_axis + "] "

    def get_plot_id(self):
        """ Get plot id

        Returns
        ------
        int
            the plot id
        """
        return self.__plot_id

    def get_function(self):
        """ Get function

        Returns
        ------
        str
            the function of the plot
        """
        return self.__name

    def set_function(self, function):
        """ Set function

        Parameters
        ------
        function
            the function
        """
        self.__function = function

    def use_function(self):
        """ Set function

        Returns
        ------
        boolean
            return the status of the use of a function
        """
        if self.__function == "":
            return False
        else:
            return True

    def get_x(self):
        """ Get x data

        Returns
        ------
        list
            the x data
        """
        return self.__x

    def set_x(self, x_data):
        """ Set x data

        Parameters
        ------
        x_data
            the x data
        """
        self.__x = x_data

    def get_y(self):
        """ Get y data

        Returns
        ------
        list
            the y data
        """
        return self.__y

    def set_y(self, y_data):
        """ Set y data

        Parameters
        ------
        y_data
            the y data
        """
        self.__y = y_data

    def get_x_axis(self):
        """ Get x axis label

        Returns
        ------
        str
            the x axis label
        """
        return self.__x_axis

    def get_y_axis(self):
        """ Get y axis label

        Returns
        ------
        str
            the y axis label
        """
        return self.__y_axis

    def get_x_unit(self):
        """ Get x unit label

        Returns
        ------
        str
            the x unit label
        """
        return self.__x_unit

    def get_y_unit(self):
        """ Get y unit label

        Returns
        ------
        str
            the y unit label
        """
        return self.__y_unit
