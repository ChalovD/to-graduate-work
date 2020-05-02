import logging
import string
from typing import List, Callable

from matplotlib import pyplot

from scr.main import PLOTS, LOG_FILE, shared


class PlotPrinter:
    def __init__(self, name: string,  x_points: List[float], calculator: Callable[[float], float]) -> None:
        self.logger = None
        self.set_up_logger()
        self.name = name
        self.storage = PLOTS.joinpath(self.name)
        self.x_points = x_points
        self.calculator = calculator
        self.x_label = 'x-label'
        self.y_label = 'y-label'

    def set_x_label(self, label: string):
        self.x_label = label

    def set_y_label(self, label: string):
        self.y_label = label

    def set_up_logger(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

        # ch = logging.StreamHandler()
        # ch.setLevel(logging.DEBUG)
        fh = logging.FileHandler(shared[LOG_FILE])
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def print(self) -> None:
        self.logger.info(f"Start to calculate y values for the plot from {self.x_points[0]} to {self.x_points[-1]} ")
        # y_points = [self.calculator(x_point) for x_point in self.x_points]

        y_points = []
        for x_point in self.x_points:
            self.logger.info(f"Start to calculate y point for x point = {x_point}")
            y_point = self.calculator(x_point)
            y_points.append(y_point)
            self.logger.info(f"The y point = {y_point} has been calculated for x point = {x_point}")
        self.logger.info(f"Y values for the plot calculated successfully")

        figure = pyplot.figure()
        axes = figure.add_axes([0.15, 0.1, 0.75, 0.8])

        axes.plot(self.x_points, y_points)
        axes.set_title(self.name)
        axes.set_xlabel(self.x_label)
        axes.set_ylabel(self.y_label)

        figure.savefig(self.storage)
        # pyplot.show()
