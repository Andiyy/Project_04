#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creating the new frame."""

from application.run import RunProgram
from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
import time


class FrameNew(QtWidgets.QFrame):
    """The visual layout of the GUI."""
    def __init__(self, data, main_window):
        QtWidgets.QFrame.__init__(self)
        self._create_widgets()
        self._connect_methods()

        self.data = data
        self.main_window = main_window

        self.run = None

    def _create_widgets(self):
        """Creating the widgets."""
        self.setFont(QtGui.QFont('Calibri', 12))

        lbl_position = QtWidgets.QLabel('Please move the weight manually to the ground:')
        lbl_start = QtWidgets.QLabel('If the weight is in the right position you can start:')

        # Buttons:
        self.pb_start = QtWidgets.QPushButton('Start')
        self.pb_up = QtWidgets.QPushButton('Up')
        self.pb_down = QtWidgets.QPushButton('Down')
        self.pb_show_diagram = QtWidgets.QPushButton('Show Graph')

        spacer_1 = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        spacer_2 = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacer_3 = QtWidgets.QSpacerItem(10, 10)

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(lbl_position, 0, 0)
        grid_layout.addWidget(self.pb_up, 0, 1)
        grid_layout.addWidget(self.pb_down, 0, 2)
        grid_layout.addItem(spacer_3, 1, 0)
        grid_layout.addWidget(lbl_start, 2, 0)
        grid_layout.addWidget(self.pb_start, 2, 1)
        grid_layout.addWidget(self.pb_show_diagram, 2, 2)
        grid_layout.addItem(spacer_1, 3, 1)
        grid_layout.addItem(spacer_2, 3, 3)

    def update_widgets(self):
        """Updating the widgets."""
        self.run = RunProgram(data=self.data)
        self.pb_show_diagram.setDisabled(True)
        self.pb_start.setEnabled(True)

    def _connect_methods(self):
        """Connecting the widgets to the methods."""
        self.pb_start.clicked.connect(self._button_start)
        self.pb_up.pressed.connect(self._button_up_pressed)
        self.pb_up.released.connect(self._button_up_released)
        self.pb_down.pressed.connect(self._button_down_pressed)
        self.pb_down.released.connect(self._button_down_released)
        self.pb_show_diagram.clicked.connect(self._button_show_diagram)

    def _button_start(self):
        """Starting the measurement."""
        self.run.run_program()
        self._write_data()
        self.pb_start.setDisabled(True)
        self.pb_show_diagram.setEnabled(True)

    def _button_up_pressed(self):
        """Moving up."""
        self.run.run(23, True)

    def _button_up_released(self):
        """Moving up."""
        self.run.run(23, False)

    def _button_down_pressed(self):
        """Moving down."""
        self.run.run(24, True)

    def _button_down_released(self):
        """Moving down."""
        self.run.run(24, False)

    def _button_show_diagram(self):
        """Showing the Diagram."""

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



