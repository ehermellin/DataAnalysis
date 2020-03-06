#!/usr/bin/python
# coding: utf-8

import logging
import re

from log.handler import logger


class MatplotlibFactory:
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if MatplotlibFactory.__instance is None:
            MatplotlibFactory()
        return MatplotlibFactory.__instance

    def __init__(self):
        if MatplotlibFactory.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            MatplotlibFactory.__instance = self

    def matplotlib_factory(self, ax, plots_list):
        self.plot(ax, plots_list)

    def matplotlib_factory(self, ax, plots_dict, plot_ids):
        plots_to_display = []
        for plot_id in plot_ids:
            pattern = re.search('id=(.+?) ', plot_id)
            if pattern:
                found = int(pattern.group(1))
                plots_to_display.append(plots_dict[found])
        self.plot(ax, plots_to_display)

    def clear(self, ax):
        ax.clear()

    def plot(self, ax, plots_to_display):
        x_data = plots_to_display[0].get_x()
        ax.clear()
        ax.set_xlabel(plots_to_display[0].get_x_axis() + " [" + plots_to_display[0].get_x_unit() + "]")

        for plot in plots_to_display:
            label = plot.get_y_axis() + "[" + plot.get_y_unit() + "]"
            ax.plot(x_data, plot.get_y(), label=label, alpha=0.50)

        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10), ncol=5, fancybox=True)
