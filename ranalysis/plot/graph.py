#!/usr/bin/python
# coding: utf-8

""" This file can be imported as a module and contains graph functions :

    * graph_from_fieldname - plot data from fieldname in a matplotlib object
    * graph_from_fieldnames - plot multiple data from fieldnames in a matplotlib object
    * graph_from_plots - plot list of plots objects in a matplotlib object
    * graph_from_plot_ids - plot list of plots from there ids in a matplotlib object
    * graph_from_data - plot data in a matplotlib object
    * graph_from_multiple_data - plot multiple data in a matplotlib object
    * clear - clear matplotlib axis object
    * plot - plot in matplotlib object

"""

import logging
import re

from ranalysis.log.loghandler import logger
from ranalysis.plot.plotcreator import PlotCreator


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
    logger.log(logging.INFO, "[Graph] Graph from fieldname")
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
    logger.log(logging.INFO, "[Graph] Graph from fieldnames")
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
    logger.log(logging.INFO, "[Graph] Graph from plots")
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
    logger.log(logging.INFO, "[Graph] Graph from plot ids")
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
    logger.log(logging.INFO, "[Graph] Graph from data")
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
    logger.log(logging.INFO, "[Graph] Graph from multiple data")
    plots_to_display = PlotCreator.get_instance().plot_from_multiple_data(x_data, y_datas, x_label, y_multiple_label)
    plot(ax, plots_to_display)


def clear(ax):
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
    x_data = plots_to_display[0].get_x()
    ax.clear()
    ax.set_xlabel(plots_to_display[0].get_x_axis() + " [" + plots_to_display[0].get_x_unit() + "]")

    for plot_tm in plots_to_display:
        label = plot_tm.get_y_axis() + "[" + plot_tm.get_y_unit() + "]"
        if len(x_data) == len(plot_tm.get_y()):
            ax.plot(x_data, plot_tm.get_y(), label=label, alpha=0.50)
        else:
            logger.log(logging.ERROR, "[Graph] x and y data do not have the same size")

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10), ncol=5, fancybox=True)
