from math import sin
from unittest import TestCase

from mpmath import linspace

from scr.plot_printers.PlotPrinter import PlotPrinter


class Test(TestCase):
    def test(self):
        x_points = linspace(0, 10, 200)
        f = sin

        plot_printer = PlotPrinter('TEST_PLOT', x_points, f)
        plot_printer.set_x_label('test_x_label')
        plot_printer.set_y_label('test_y_label')
        plot_printer.print()
