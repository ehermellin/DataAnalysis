#!/usr/bin/python
# coding: utf-8


class Plot:

    def __init__(self, plot_id, x, y, x_axis="", y_axis="", x_unit="", y_unit=""):
        self.__plot_id = plot_id
        self.__x = x
        self.__y = y
        self.__x_axis = x_axis
        self.__y_axis = y_axis
        self.__x_unit = x_unit
        self.__y_unit = y_unit

    def __str__(self):
        return "id=" + str(self.__plot_id) + " [" + self.__x_axis + " | " + self.__y_axis + "]"

    def get_plot_id(self):
        return self.__plot_id

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_x_axis(self):
        return self.__x_axis

    def get_y_axis(self):
        return self.__y_axis

    def get_x_unit(self):
        return self.__x_unit

    def get_y_unit(self):
        return self.__y_unit

    def print_plot(self):
        print(self.__plot_id)
        print(self.__x)
        print(self.__y)
        print(self.__x_axis)
        print(self.__y_axis)
        print(self.__x_unit)
        print(self.__y_unit)
