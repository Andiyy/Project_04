# -*- coding: utf-8 -*-

"""Creating the open frame."""

from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np


class FrameOpen(QtWidgets.QFrame):
    """The visual layout of the GUI."""

    def __init__(self, data):
        QtWidgets.QFrame.__init__(self)

        self.data = data

        self._x_time = None
        self._y_voltage = None
        self._y_current = None

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
        self.list_widget.doubleClicked.connect(self.lw_open_old)

    def lw_open_old(self):
        """Open the old measurement."""
        index = self.list_widget.currentRow()
        self.data.plot_measurement['m_header'] = self.data.old_measurement[index]

        step = self.data.plot_measurement['m_header'].h_step
        amount_steps = int(5 / step + 1)
        self._x_time = np.arange(0, 5.001, step)
        self._y_voltage = np.zeros(amount_steps)
        self._y_current = np.zeros(amount_steps)

        # Database:
        with open_sqlite3() as cursor:
            cursor.execute('SELECT d_value FROM m_data WHERE h_id=? AND s_id=?',
                           (self.data.plot_measurement['m_header'].h_id, 1))
            data = cursor.fetchall()

        for line, row in enumerate(data):
            self._y_current[line] = row[0]

        with open_sqlite3() as cursor:
            cursor.execute('SELECT d_value FROM m_data WHERE h_id=? AND s_id=?',
                           (self.data.plot_measurement['m_header'].h_id, 2))
            data = cursor.fetchall()

        for line, row in enumerate(data):
            self._y_voltage[line] = row[0]

        self.plot_data()

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

    def plot_data(self):
        """Showing the data in a plot."""
        plt.subplot(2, 1, 1)
        plt.plot(self._x_time, self._y_current, 'o-')
        plt.title('Strom-Zeit-Diagramm')
        plt.xlabel('Zeit in s')
        plt.ylabel('Strom in A')

        plt.subplot(2, 1, 2)
        plt.plot(self._x_time, self._y_voltage, 'o-')
        plt.title('Spannung-Zeit-Diagramm')
        plt.xlabel('Zeit in s')
        plt.ylabel('Spannung in V')

        plt.show()

