# -*- coding: utf-8 -*-

"""Creating the Plot frame."""

from PyQt5 import QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class FramePlot(QtWidgets.QFrame):
    """The visual layout of the GUI."""

    def __init__(self, data):
        QtWidgets.QFrame.__init__(self)
        self.data = data

        self._create_widgets()

    def _create_widgets(self):
        """Crating the widgets."""
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.pb_close = QtWidgets.QPushButton('Close')
        self.pb_close.clicked.connect(self._button_close)

        # Layout:
        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(self.toolbar)
        grid_layout.addWidget(self.canvas)
        grid_layout.addWidget(self.pb_close)

    def plot(self):
        """Plotting the data."""
        self.figure.clear()

        ax = self.figure.add_subplot(111)
        ax.plot(self.data.plot_measurement['Time'], self.data.plot_measurement['Voltage'], '*-')

        ax = self.figure.add_subplot(111)
        ax.plot(self.data.plot_measurement['Time'], self.data.plot_measurement['Current'], '*-')

        # refresh canvas
        self.canvas.draw()

    def _button_close(self):
        """Closing the frame."""
