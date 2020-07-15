# -*- coding: utf-8 -*-

"""Creating the open frame."""

from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
from collections import namedtuple
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


class FrameOpen(QtWidgets.QFrame):
    """The visual layout of the GUI."""

    def __init__(self, data, main_window):
        QtWidgets.QFrame.__init__(self)

        self.data = data
        self.main_window = main_window

        self.setFont(QtGui.QFont('Calibri', 12))

        self._create_widgets()
        self._connect_methods()
        self.lw_load_data()

    def _create_widgets(self):
        """Crating the widgets of the frame."""
        self.list_widget = QtWidgets.QListWidget()

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(self.list_widget)

    def _connect_methods(self):
        """Connecting the widgets to the methods."""
        self.list_widget.doubleClicked.connect(self._lw_open_old)

    def _lw_open_old(self):
        """Open the old measurement."""
        index = self.list_widget.currentRow()
        self.data.plot_measurement['m_header'] = self.data.old_measurement[index]

        amount_steps = self.data.plot_measurement['m_header'].h_length * 100 + 150

        self.data.plot_measurement['Time'] = np.arange(0, self.data.plot_measurement['m_header'].h_length + 1.5, 0.01)
        self.data.plot_measurement['Current'] = np.zeros(amount_steps)
        self.data.plot_measurement['Voltage'] = np.zeros(amount_steps)
        self.data.plot_measurement['Power'] = np.zeros(amount_steps)
        self.data.plot_measurement['RPM'] = np.zeros(self.data.plot_measurement['m_header'].h_length * 2 + 3)
        self.data.plot_measurement['rpm_time'] = np.arange(0, self.data.plot_measurement['m_header'].h_length + 1.5, 0.5)

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

        with open_sqlite3() as cursor:
            cursor.execute('SELECT d_value FROM m_data WHERE h_id=? AND s_id=?',
                           (self.data.plot_measurement['m_header'].h_id, 3))
            data = cursor.fetchall()

        for line, row in enumerate(data):
            self.data.plot_measurement['RPM'][line] = row[0]

        self._calculate_power()
        self._plot()

    def _calculate_power(self):
        """"""
        for index in range(len(self.data.plot_measurement['Power'])):
            self.data.plot_measurement['Power'][index] = \
                self.data.plot_measurement['Current'][index] * self.data.plot_measurement['Voltage'][index]

    def test(self):
        """"""
        average_power = []  # np.zeros(int(len(power)/50))
        reset_counter = np.arange(0, len(self.data.plot_measurement['Power']), 50)

        counter = 0

        for index, item in enumerate(self.data.plot_measurement['Power']):
            counter += item
            if index in reset_counter:
                counter /= 50
                average_power.append(counter)
                counter = 0

        moment = np.zeros(len(average_power))

        for i in range(len(moment)):
            moment[i] = (average_power[i] * 9.55) / self.data.plot_measurement['RPM'][i]

        fig, ax = plt.subplots()
        ax.plot(np.arange(len(average_power)), average_power)
        ax.plot(np.arange(len(average_power)), self.data.plot_measurement['RPM'])
        ax.plot(np.arange(len(average_power)), moment)

        ax.grid()
        plt.show()

    def _plot(self):
        """Opening the plot."""
        # self.test()

        sns.set_style('whitegrid')

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)
        #

        fig.dpi = 100

        ax1.plot(self.data.plot_measurement['Time'], self.data.plot_measurement['Voltage'], '-', color='b')
        ax1.set_xlabel('Time in s')
        ax1.set_ylabel('Voltage in V')

        ax2.plot(self.data.plot_measurement['Time'], self.data.plot_measurement['Current'], '-', color='r')
        ax2.set_xlabel('Time in s')
        ax2.set_ylabel('Current in A')

        ax3.plot(self.data.plot_measurement['rpm_time'], self.data.plot_measurement['RPM'], '*-', color='y')
        ax3.set_xlabel('Time in s')
        ax3.set_ylabel('RPM in 1/min')

        ax4.plot(self.data.plot_measurement['Time'], self.data.plot_measurement['Power'], '-', color='g')
        ax4.set_xlabel('Time in s')
        ax4.set_ylabel('Power in W')

        plt.show()

    def lw_load_data(self):
        """Loading the data into the list widget."""
        m_header = namedtuple('m_header', ['h_id', 'u_id', 'h_date', 'h_weight', 'h_length'])

        self.data.old_measurement.clear()
        self.list_widget.clear()

        # Database:
        with open_sqlite3() as cursor:
            cursor.execute('SELECT h_id, u_id, h_date, h_weight, h_length FROM m_header ORDER BY h_id DESC')
            data = cursor.fetchall()

        for row in data:
            self.data.old_measurement.append(m_header(*row))
            self.list_widget.addItem(f'ID: {row[0]} | Date: {row[2]} | Weight: {row[3]}')
