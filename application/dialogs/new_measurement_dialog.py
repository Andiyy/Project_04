#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Widgets for the main window."""

from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
from collections import namedtuple
import datetime


class NewMeasurement(QtWidgets.QDialog):
    """The visual layout of the GUI."""
    def __init__(self, *args, **kwargs):
        super(NewMeasurement, self).__init__(*args, **kwargs)

        self.data = None

        self.create_widgets()

    def create_widgets(self):
        """Creating the widgets."""
        self.setWindowTitle('New Measurement')
        self.setFont(QtGui.QFont('Calibri', 12))

        lbl_weight = QtWidgets.QLabel('Weight:')
        self.sb_weight = QtWidgets.QSpinBox()
        self.sb_weight.setMaximum(10)

        lbl_test_step = QtWidgets.QLabel('Steps:')
        self.sb_step = QtWidgets.QDoubleSpinBox()
        self.sb_step.setSingleStep(0.01)
        self.sb_step.setMaximum(1)

        self.pb_create = QtWidgets.QPushButton()
        self.pb_create.setText('Create')
        self.pb_create.clicked.connect(self._button_create)

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(lbl_weight, 0, 0)
        grid_layout.addWidget(self.sb_weight, 0, 1)
        grid_layout.addWidget(lbl_test_step, 1, 0)
        grid_layout.addWidget(self.sb_step, 1, 1)
        grid_layout.addWidget(self.pb_create, 2, 1)

    def set_data(self, data):
        """Creating the data object."""
        self.data = data

    def _button_create(self):
        """Button Start."""
        weight = self.sb_weight.value()
        step = self.sb_step.value()

        self._create_new_measurement(weight=weight, step=step)

        self.accept()

    def _create_new_measurement(self, weight: int, step: float):
        """Creating a new measurement in the database."""
        tuple_data = namedtuple('m_header', ['h_id', 'u_id', 'h_date', 'h_weight', 'h_step'])

        h_id = len(self.data.old_measurement)
        h_date = str(datetime.datetime.today())[:9]

        self.data.new_measurement = tuple_data(h_id, self.data.user.u_id, h_date, weight, step)

        with open_sqlite3() as cursor:
            cursor.execute('INSERT INTO m_header VALUES (?, ?, ?, ?, ?) ', self.data.new_measurement)
