# -*- coding: utf-8 -*-

"""Creating the open frame."""

from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np


class FrameOpen(QtWidgets.QFrame):
    """The visual layout of the GUI."""

    def __init__(self, data, main_window):
        QtWidgets.QFrame.__init__(self)

        self.data = data
        self.main_window = main_window

        self.setFont(QtGui.QFont('Calibri', 12))

        self.create_widgets()
        self.connect_methods()
        self.lw_load_data()

    def create_widgets(self):
        """Crating the widgets of the frame."""
        self.list_widget = QtWidgets.QListWidget()

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(self.list_widget)

    def connect_methods(self):
        """Connecting the widgets to the methods."""
        self.list_widget.doubleClicked.connect(self._lw_open_old)

    def _lw_open_old(self):
        """Open the old measurement."""
        index = self.list_widget.currentRow()
        self.data.plot_measurement['m_header'] = self.data.old_measurement[index]

        step = self.data.plot_measurement['m_header'].h_step
        amount_steps = int(5 / step + 1)

        self.data.plot_measurement['Time'] = np.arange(0, 5.001, step)
        self.data.plot_measurement['Current'] = np.zeros(amount_steps)
        self.data.plot_measurement['Voltage'] = np.zeros(amount_steps)

        # Database:
        with open_sqlite3() as cursor:
            cursor.execute('SELECT d_value FROM m_data WHERE h_id=? AND s_id=?',
                           (self.data.plot_measurement['m_header'].h_id, 1))
            data = cursor.fetchall()

        for line, row in enumerate(data):
            self.data.plot_measurement['Current'][line] = row[0]

        with open_sqlite3() as cursor:
            cursor.execute('SELECT d_value FROM m_data WHERE h_id=? AND s_id=?',
                           (self.data.plot_measurement['m_header'].h_id, 2))
            data = cursor.fetchall()

        for line, row in enumerate(data):
            self.data.plot_measurement['Voltage'][line] = row[0]

        self.open_plot()

    def open_plot(self):
        """Opening the plot frame."""
        self.main_window.central_layout.removeWidget(self)
        self.hide()

        self.main_window.central_layout.addWidget(self.main_window.frame_plot, 2, 2, 1, 2)
        self.main_window.frame_plot.show()
        self.main_window.frame_plot.plot()

    def lw_load_data(self):
        """Loading the data into the list widget."""
        m_header = namedtuple('m_header', ['h_id', 'u_id', 'h_date', 'h_weight', 'h_step'])

        self.data.old_measurement.clear()
        self.list_widget.clear()

        # Database:
        with open_sqlite3() as cursor:
            cursor.execute('SELECT h_id, u_id, h_date, h_weight, h_step FROM m_header')
            data = cursor.fetchall()

        for row in data:
            self.data.old_measurement.append(m_header(*row))
            self.list_widget.addItem(f'ID: {row[0]} | Date: {row[2]} | Weight: {row[3]}')
