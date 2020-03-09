#!/usr/bin/python
# coding: utf-8

import logging
import re

from log.loghandler import logger
from plot.plotcreator import PlotCreator


def graph_from_fieldname(ax, manager, x_fieldname, y_fieldname):
    logger.log(logging.INFO, "[Graph] Graph from fieldname")
    plots = [PlotCreator.get_instance().plot_from_fieldname(manager, x_fieldname, y_fieldname)]
    plot(ax, plots)


def graph_from_fieldnames(ax, manager, x_fieldname, y_fieldnames):
    logger.log(logging.INFO, "[Graph] Graph from fieldnames")
    plots = PlotCreator.get_instance().plot_from_fieldnames(manager, x_fieldname, y_fieldnames)
    plot(ax, plots)


def graph_from_plots(ax, list_plots):
    logger.log(logging.INFO, "[Graph] Graph from plots")
    plot(ax, list_plots)


def graph_from_plot_ids(ax, plot_ids):
    logger.log(logging.INFO, "[Graph] Graph from plot ids")
    plots_to_display = []
    for plot_id in plot_ids:
        pattern = re.search('id=(.+?) ', plot_id)
        if pattern:
            found = int(pattern.group(1))
            plots_to_display.append(PlotCreator.get_instance().get_plots_dict()[found])
    plot(ax, plots_to_display)


def graph_from_data(ax, x_data, y_data, x_label, y_label):
    logger.log(logging.INFO, "[Graph] Graph from data")
    plots_to_display = [PlotCreator.get_instance().plot_from_data(x_data, y_data, x_label, y_label)]
    plot(ax, plots_to_display)


def graph_from_multiple_data(ax, x_data, y_datas, x_label, y_label):
    logger.log(logging.INFO, "[Graph] Graph from data")
    plots_to_display = PlotCreator.get_instance().plot_from_multiple_data(x_data, y_datas, x_label, y_label)
    plot(ax, plots_to_display)


def clear(ax):
    ax.clear()


def plot(ax, plots_to_display):
    x_data = plots_to_display[0].get_x()
    ax.clear()
    ax.set_xlabel(plots_to_display[0].get_x_axis() + " [" + plots_to_display[0].get_x_unit() + "]")

    for plot_tm in plots_to_display:
        label = plot_tm.get_y_axis() + "[" + plot_tm.get_y_unit() + "]"
        ax.plot(x_data, plot_tm.get_y(), label=label, alpha=0.50)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10), ncol=5, fancybox=True)
