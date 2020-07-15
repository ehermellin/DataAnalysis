#!/usr/bin/python
# coding: utf-8

""" This file can be imported as a module and contains graph functions :

    * graph_from_function - create plot from math functions
    * graph_from_fieldname - plot data from fieldname in a matplotlib object
    * graph_from_fieldnames - plot multiple data from fieldnames in a matplotlib object
    * graph_from_plots - plot list of plots objects in a matplotlib object
    * graph_from_plot_ids - plot list of plots from there ids in a matplotlib object
    * graph_from_data - plot data in a matplotlib object
    * graph_from_multiple_data - plot multiple data in a matplotlib object
    * graph_add_title - add title to the graph
    * graph_compare_plot - fill between two plots (compare two plots)
    * graph_compare_plot_diff - plot the diff between two plots
    * graph_compare_plot_values - plot the diff values between two plots
    * graph_clear - clear matplotlib axis object
    * plot - plot in matplotlib object

"""

import logging
import re

from ranalysis.log.loghandler import logger
from ranalysis.plot.plotcreator import PlotCreator


def graph_from_function(ax, function_list):
    """ Plot data from fieldname in a matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    function_list : list(function)
        the list of function to plot
    """
    logger.log(logging.DEBUG, "[Graph] Graph from function")
    for func in function_list:
        function_to_plot = PlotCreator.get_instance().string_to_function(func.get_function())
        ax.plot(func.get_interval(), function_to_plot(func.get_interval()))


def graph_from_function(ax, function, xmin, xmax, discr, xlabel="", ylabel=""):
    """ Plot mathematic function

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    function : str
        the mathematic function
    xmin :  int
        the x min
    xmax : int
        the x max
    discr : int
        the discretization of the interval between xmin and xmax
    xlabel :  str
        the name of the x label
    ylabel : str
        the name of the y label
    """
    logger.log(logging.DEBUG, "[Graph] Graph from function")
    plots = [PlotCreator.get_instance().plot_from_function(function, xmin, xmax, discr, xlabel, ylabel)]
    plot(ax, plots)


def graph_from_fieldname(ax, manager, x_fieldname, y_fieldname):
    """ Plot data from fieldname in a matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    manager : DataManager
        the data manager used to read data from csv file
    x_fieldname : str
        the fieldname of the x-axis variable to plot
    y_fieldname : str
        the fieldname of the y-axis variable to plot
    """
    logger.log(logging.DEBUG, "[Graph] Graph from fieldname")
    plots = [PlotCreator.get_instance().plot_from_fieldname(manager, x_fieldname, y_fieldname)]
    plot(ax, plots)


def graph_from_fieldnames(ax, manager, x_fieldname, y_fieldnames):
    """ Plot multiple data from fieldnames in a matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    manager : DataManager
        the data manager used to read data from csv file
    x_fieldname : str
        the fieldname of the x-axis variable to plot
    y_fieldnames : list(str)
        the list of fieldname of the y-axis variable to plot
    """
    logger.log(logging.DEBUG, "[Graph] Graph from fieldnames")
    plots = PlotCreator.get_instance().plot_from_fieldnames(manager, x_fieldname, y_fieldnames)
    plot(ax, plots)


def graph_from_plots(ax, list_plots):
    """ Plot list of plots objects in a matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    list_plots : list(plot)
        the list of plot
    """
    logger.log(logging.DEBUG, "[Graph] Graph from plots")
    plot(ax, list_plots)


def graph_from_plot_ids(ax, plot_ids):
    """ Plot list of plots from there ids in a matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    plot_ids : list(int)
        the list of plot ids
    """
    logger.log(logging.DEBUG, "[Graph] Graph from plot ids")
    plots_to_display = []
    for plot_id in plot_ids:
        pattern = re.search('id=(.+?) ', plot_id)
        if pattern:
            found = int(pattern.group(1))
            plots_to_display.append(PlotCreator.get_instance().get_plots_dict()[found])
    plot(ax, plots_to_display)


def graph_from_data(ax, x_data, y_data, x_label, y_label):
    """ Plot data in a matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    x_data :  list(int, float, ...)
        list of data (x-axis)
    y_data : list(int, float, ...)
        list of data (y-axis)
    x_label : str
        the label of the x-axis
    y_label : str
        the label of the y-axis
    """
    logger.log(logging.DEBUG, "[Graph] Graph from data")
    plots_to_display = [PlotCreator.get_instance().plot_from_data(x_data, y_data, x_label, y_label)]
    plot(ax, plots_to_display)


def graph_from_multiple_data(ax, x_data, y_datas, x_label, y_multiple_label):
    """ Plot data in a matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    x_data :  list(int, float, ...)
        list of data (x-axis)
    y_datas : list(list(int, float, ...))
        multiple list of data (y-axis)
    x_label : str
        the label of the x-axis
    y_multiple_label : str
        the list of label of the y-axis
    """
    logger.log(logging.DEBUG, "[Graph] Graph from multiple data")
    plots_to_display = PlotCreator.get_instance().plot_from_multiple_data(x_data, y_datas, x_label, y_multiple_label)
    plot(ax, plots_to_display)


def graph_add_title(ax, title):
    """ Add title to the graph

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    title : str
        the title of the graph
    """
    ax.set_title(title)


def graph_compare_plot(ax, plot1, plot2):
    """ Fill between two plots (compare two plots)

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    plot1 : Plot
        the first plot to compare
    plot2 : Plot
        the second plot to compare
    """
    ax.clear()

    plot(ax, [plot1, plot2])

    ax.fill_between(plot1.get_x(), plot1.get_y(), plot2.get_y(), color='grey', alpha='0.3')

    ax.legend(loc='upper center', bbox_to_anchor=(1.05, 0.75), ncol=1, fancybox=True)


def graph_compare_plot_diff(ax, plot1, plot2):
    """ Plot the diff between two plots

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    plot1 : Plot
        the first plot to compare
    plot2 : Plot
        the second plot to compare
    """
    diff = []
    compar_dif = []
    for ii in range(len(plot1.get_x())):
        diff.append(abs(plot1.get_y()[ii] - plot2.get_y()[ii]))
        compar_dif.append(0)

    label = "Difference between plots"

    ax.plot(plot1.get_x(), diff, label=label, alpha=0.50)
    ax.plot(plot1.get_x(), compar_dif, alpha=0.50)

    ax.fill_between(plot1.get_x(), diff, compar_dif, color='red', alpha='0.3')


def graph_compare_plot_values(ax, plot1, plot2):
    """ Plot the diff values between two plots

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    plot1 : Plot
        the first plot to compare
    plot2 : Plot
        the second plot to compare
    """
    ymin = min(plot1.get_y())
    for ii in range(len(plot1.get_x())):
        value = abs(plot1.get_y()[ii] - plot2.get_y()[ii])
        ax.text(plot1.get_x()[ii] - 0.1, value, round(value, 2), size=8)


def graph_clear(ax):
    """ Clear matplotlib axis object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    """
    ax.clear()


def plot(ax, plots_to_display):
    """  Plot in matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    plots_to_display : list(plot)
        the list of plots to plot
    """

    ax.set_xlabel(plots_to_display[0].get_x_axis() + " [" + plots_to_display[0].get_x_unit() + "]")

    for plot_tm in plots_to_display:
        label = plot_tm.get_y_axis() + " [" + plot_tm.get_y_unit() + "]"
        ax.plot(plot_tm.get_x(), plot_tm.get_y(), label=label, alpha=0.50)

    ax.legend(loc='upper center', bbox_to_anchor=(1.05, 0.75), ncol=1, fancybox=True)
