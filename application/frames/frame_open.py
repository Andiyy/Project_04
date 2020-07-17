# -*- coding: utf-8 -*-

"""Creating the open frame."""

from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
from collections import namedtuple
import numpy as np
import seaborn as sns
import matplotlib
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
        """Open the old measurement.

        Creting all arrays:
        Nucleo:     100Hz
        Idle:       1s at the start/end

        amount_steps:   *100    -> Nucleo
                        +200    -> idle
        Time:           +2      -> idle
                        0.01    -> Nucleo
        RPM:            *2      -> Average all 0.5 seconds
                        +5      -> idle
        rpm_time:       +2.5    -> idle
                        0.5     -> Average all 0.5 seconds

        Downloading data from the database.
        """
        index = self.list_widget.currentRow()
        self.data.plot_measurement['m_header'] = self.data.old_measurement[index]

        amount_steps = self.data.plot_measurement['m_header'].h_length * 100 + 200

        self.data.plot_measurement['Time'] = np.arange(0, self.data.plot_measurement['m_header'].h_length + 2, 0.01)
        self.data.plot_measurement['Current'] = np.zeros(amount_steps)
        self.data.plot_measurement['Voltage'] = np.zeros(amount_steps)
        self.data.plot_measurement['Power'] = np.zeros(amount_steps)
        self.data.plot_measurement['RPM'] = np.zeros(self.data.plot_measurement['m_header'].h_length * 2 + 5)
        self.data.plot_measurement['rpm_time'] = \
            np.arange(0, self.data.plot_measurement['m_header'].h_length + 2.5, 0.5)

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
        """Calculating the power."""
        for index in range(len(self.data.plot_measurement['Power'])):
            self.data.plot_measurement['Power'][index] = \
                self.data.plot_measurement['Current'][index] * self.data.plot_measurement['Voltage'][index]

    def _calculate_moment(self):
        """Calculating the moment.
        NOT USED!

        Calculating the average power and rpm and then calculating the moment.
        """
        print("Current: ")
        print(sum(self.data.plot_measurement['Current'][74:-120]) / len(self.data.plot_measurement['Current'][74:-120]))

        ap = sum(self.data.plot_measurement['Power'][74:-120])/len(self.data.plot_measurement['Power'][74:-120])
        arpm = sum(self.data.plot_measurement['RPM'][2:-2])/len(self.data.plot_measurement['RPM'][2:-2])

        print("Moment: ")
        print(ap*9.55/arpm)

    def _plot(self):
        """Opening the plot."""
        matplotlib.rcParams.update({'font.size': 25})

        # self._calculate_moment()

        sns.set_style('whitegrid')

        fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)

        fig.dpi = 100

        ax1.set_title(f'{self.data.plot_measurement["m_header"].h_weight} - kg')

        ax1.plot(self.data.plot_measurement['Time'], self.data.plot_measurement['Voltage'], '-', color='b')
        ax1.set_ylabel('Voltage in V')

        ax2.plot(self.data.plot_measurement['Time'], self.data.plot_measurement['Current'], '-', color='r')
        ax2.set_ylabel('Current in A')

        ax3.plot(self.data.plot_measurement['Time'], self.data.plot_measurement['Power'], '-', color='g')
        ax3.set_ylabel('Power in W')

        ax4.plot(self.data.plot_measurement['rpm_time'], self.data.plot_measurement['RPM'], '*-', color='y')
        ax4.set_xlabel('Time in s')
        ax4.set_ylabel('RPM in 1/min')

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
