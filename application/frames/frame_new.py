#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creating the new frame."""

from application.run.run import RunProgram
from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui


class FrameNew(QtWidgets.QFrame):
    """The visual layout of the GUI."""
    def __init__(self, data):
        QtWidgets.QFrame.__init__(self)
        self._create_widgets()
        self._connect_methods()

        self.data = data
        self.run = None

    def _create_widgets(self):
        """Creating the widgets."""
        self.setFont(QtGui.QFont('Calibri', 12))

        # Buttons:
        self.pb_start = QtWidgets.QPushButton('Start')
        self.pb_up = QtWidgets.QPushButton('Up')
        self.pb_down = QtWidgets.QPushButton('Down')

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(self.pb_start)
        grid_layout.addWidget(self.pb_up)
        grid_layout.addWidget(self.pb_down)

    def update_widgets(self):
        """Updating the widgets."""

    def _connect_methods(self):
        """Connecting the widgets to the methods."""
        self.pb_start.clicked.connect(self._button_start)
        self.pb_up.clicked.connect(self._button_up)
        self.pb_down.clicked.connect(self._button_down)

    def _button_start(self):
        """Starting the measurement."""
        self.run = RunProgram(data=self.data)
        self.run.run_program()

        self._write_data()

    def _button_up(self):
        """Moving up."""

    def _button_down(self):
        """Moving down."""

    def _write_data(self):
        """'Writing the data into the database."""
        with open_sqlite3() as cursor:
            for value in self.data.measured_values['Current']:
                cursor.execute('INSERT INTO m_data VALUES (?, ?, ?);',
                               (self.data.new_measurement.h_id, 1, value))

        with open_sqlite3() as cursor:
            for value in self.data.measured_values['Voltage']:
                cursor.execute('INSERT INTO m_data VALUES (?, ?, ?);',
                               (self.data.new_measurement.h_id, 2, value))

        # with open_sqlite3() as cursor:
        # cursor.execute('INSERT INTO m_data VALUES (?, ?, ?);',
        #                (self.data.new_measurement.h_id, 3, self.data.measured_values['Current']))



