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
    * graph_compare_plot_from_fieldnames - fill between two plots (compare two plots)
    * graph_compare_plot_diff_from_fieldnames - plot the diff between two plots
    * graph_compare_plot_values_from_fieldnames - plot the diff values between two plots
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


def graph_from_function(ax, function_list, marker="."):
    """ Plot data from fieldname in a matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    function_list : list(function)
        the list of function to plot
    marker : string
        the style of the marker to plot
    """
    logger.log(logging.INFO, "[Graph] Graph from function")
    for func in function_list:
        function_to_plot = PlotCreator.get_instance().string_to_function(func.get_function())
        ax.plot(func.get_interval(), function_to_plot(func.get_interval()), marker=marker)


def graph_from_function(ax, function, xmin, xmax, discr, xlabel="", ylabel="", marker="."):
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
    marker : string
        the style of the marker to plot
    """
    logger.log(logging.INFO, "[Graph] Graph from function")
    plots = [PlotCreator.get_instance().plot_from_function(function, xmin, xmax, discr, xlabel, ylabel)]
    plot(ax, plots, marker)


def graph_from_fieldname(ax, manager, x_fieldname, y_fieldname, marker="."):
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
    marker : string
        the style of the marker to plot
    """
    logger.log(logging.INFO, "[Graph] Graph from fieldname")
    plots = [PlotCreator.get_instance().plot_from_fieldname(manager, x_fieldname, y_fieldname)]
    plot(ax, plots, marker)


def graph_from_fieldnames(ax, manager, x_fieldname, y_fieldnames, marker="."):
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
    marker : string
        the style of the marker to plot
    """
    logger.log(logging.INFO, "[Graph] Graph from fieldnames")
    plots = PlotCreator.get_instance().plot_from_fieldnames(manager, x_fieldname, y_fieldnames)
    plot(ax, plots, marker)


def graph_from_plots(ax, list_plots, marker="."):
    """ Plot list of plots objects in a matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    list_plots : list(plot)
        the list of plot
    marker : string
        the style of the marker to plot
    """
    logger.log(logging.INFO, "[Graph] Graph from plots")
    plot(ax, list_plots, marker)


def graph_from_plot_ids(ax, plot_ids, marker="."):
    """ Plot list of plots from there ids in a matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    plot_ids : list(int)
        the list of plot ids
    marker : string
        the style of the marker to plot
    """
    logger.log(logging.INFO, "[Graph] Graph from plot ids")
    plots_to_display = []
    for plot_id in plot_ids:
        pattern = re.search('id=(.+?) ', plot_id)
        if pattern:
            found = int(pattern.group(1))
            plots_to_display.append(PlotCreator.get_instance().get_plots_dict()[found])
    plot(ax, plots_to_display, marker)


def graph_from_data(ax, x_data, y_data, x_label, y_label, marker="."):
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
    marker : string
        the style of the marker to plot
    """
    logger.log(logging.INFO, "[Graph] Graph from data")
    plots_to_display = [PlotCreator.get_instance().plot_from_data(x_data, y_data, x_label, y_label)]
    plot(ax, plots_to_display, marker)


def graph_from_multiple_data(ax, x_data, y_datas, x_label, y_multiple_label, marker="."):
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
    marker : string
        the style of the marker to plot
    """
    logger.log(logging.INFO, "[Graph] Graph from multiple data")
    plots_to_display = PlotCreator.get_instance().plot_from_multiple_data(x_data, y_datas, x_label, y_multiple_label)
    plot(ax, plots_to_display, marker)


def graph_add_title(ax, title):
    """ Add title to the graph

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    title : str
        the title of the graph
    """
    logger.log(logging.INFO, "[Graph] Clear")
    ax.set_title(title)


def graph_compare_plot_from_fieldnames(ax, manager, x_fieldname, y_fieldnames, marker="."):
    """ Fill between two plots (compare two plots)

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
    marker : string
        the style of the marker to plot
    """
    plots = PlotCreator.get_instance().plot_from_fieldnames(manager, x_fieldname, y_fieldnames)
    if len(plots) == 2:
        graph_compare_plot(ax, plots[0], plots[1], marker)
    else:
        logger.log(logging.ERROR, "[Graph] You can only compare two graphs (" + str(len(plots)) + " given)")


def graph_compare_plot(ax, plot1, plot2, marker="."):
    """ Fill between two plots (compare two plots)

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    plot1 : Plot
        the first plot to compare
    plot2 : Plot
        the second plot to compare
    marker : string
        the style of the marker to plot
    """
    logger.log(logging.INFO, "[Graph] Compare two plots")
    plot(ax, [plot1, plot2], marker)
    ax.fill_between(plot1.get_x(), plot1.get_y(), plot2.get_y(), color='grey', alpha=0.3)
    ax.legend(loc='upper center', bbox_to_anchor=(1.05, 0.75), ncol=1, fancybox=True)


def graph_compare_plot_diff_from_fieldnames(ax, manager, x_fieldname, y_fieldnames, marker="."):
    """ Plot the diff between two plots

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
    marker : string
        the style of the marker to plot
    """
    plots = PlotCreator.get_instance().plot_from_fieldnames(manager, x_fieldname, y_fieldnames)
    if len(plots) == 2:
        graph_compare_plot_diff(ax, plots[0], plots[1], marker)
    else:
        logger.log(logging.ERROR, "[Graph] You can only compare two graphs (" + str(len(plots)) + " given)")


def graph_compare_plot_diff(ax, plot1, plot2, marker="."):
    """ Plot the diff between two plots

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    plot1 : Plot
        the first plot to compare
    plot2 : Plot
        the second plot to compare
    marker : string
        the style of the marker to plot
    """
    logger.log(logging.INFO, "[Graph] Display compare graph")
    diff = []
    compar_dif = []
    for ii in range(len(plot1.get_x())):
        diff.append(abs(plot1.get_y()[ii] - plot2.get_y()[ii]))
        compar_dif.append(0)

    label = "Difference between plots"

    ax.plot(plot1.get_x(), diff, label=label, alpha=0.50, marker=marker)
    ax.plot(plot1.get_x(), compar_dif, alpha=0.50, marker=marker)

    ax.fill_between(plot1.get_x(), diff, compar_dif, color='red', alpha=0.3)


def graph_compare_plot_values_from_fieldnames(ax, manager, x_fieldname, y_fieldnames, threshold, on_graph):
    """ Plot the diff values between two plots

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
    threshold :
        the threshold for the display of the difference values
    on_graph :
        display the values on the graph or not
    """
    plots = PlotCreator.get_instance().plot_from_fieldnames(manager, x_fieldname, y_fieldnames)
    if len(plots) == 2:
        graph_compare_plot_values(ax, plots[0], plots[1], threshold, on_graph)
    else:
        logger.log(logging.ERROR, "[Graph] You can only compare two graphs (" + str(len(plots)) + " given)")


def graph_compare_plot_values(ax, plot1, plot2, threshold, on_graph, round_value=2):
    """ Plot the diff values between two plots

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    plot1 : Plot
        the first plot to compare
    plot2 : Plot
        the second plot to compare
    threshold : float
        the threshold to print the difference value
    on_graph : boolean
        plot on graph or on the x axis
    round_value : int
        the number of decimal to use
    """
    logger.log(logging.INFO, "[Graph] Display compare values")
    ymin = min(plot1.get_y())
    for ii in range(len(plot1.get_x())):
        value = abs(plot1.get_y()[ii] - plot2.get_y()[ii])
        if value > threshold:
            y_pos = ymin * 0.99
            if on_graph:
                y_pos = value

            ax.text(plot1.get_x()[ii] - 0.1, y_pos, round(value, round_value), size=8)


def graph_clear(ax):
    """ Clear matplotlib axis object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    """
    ax.clear()


def plot(ax, plots_to_display, marker="."):
    """  Plot in matplotlib object

    Parameters
    ----------
    ax : Axis
        the matplotlib axis object
    plots_to_display : list(plot)
        the list of plots to plot
    marker : string
        the style of the marker to plot
    """

    ax.set_xlabel(plots_to_display[0].get_x_axis() + " [" + plots_to_display[0].get_x_unit() + "]")

    for plot_tm in plots_to_display:
        label = plot_tm.get_y_axis() + " [" + plot_tm.get_y_unit() + "]"
        ax.plot(plot_tm.get_x(), plot_tm.get_y(), label=label, alpha=0.50, marker=marker)

    ax.legend(loc='upper center', bbox_to_anchor=(1.05, 0.75), ncol=1, fancybox=True)
