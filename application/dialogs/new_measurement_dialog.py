# -*- coding: utf-8 -*-

"""Dialog to create a new measurement."""

from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
from collections import namedtuple
import datetime


class NewMeasurement(QtWidgets.QDialog):
    """Dialog - new measurement."""
    def __init__(self, *args, **kwargs):
        super(NewMeasurement, self).__init__(*args, **kwargs)

        self.data = None
        self._create_widgets()

    def _create_widgets(self):
        """Creating the widgets."""
        self.setWindowTitle('New Measurement')
        self.setFont(QtGui.QFont('Calibri', 12))

        lbl_weight = QtWidgets.QLabel('Weight:')
        self.sb_weight = QtWidgets.QDoubleSpinBox()
        self.sb_weight.setMaximum(10)

        lbl_length = QtWidgets.QLabel('Length:')
        self.sb_length = QtWidgets.QSpinBox()
        self.sb_length.setMinimum(1)
        self.sb_length.setMaximum(7)
        self.sb_length.setValue(7)

        self.pb_create = QtWidgets.QPushButton('Create')
        self.pb_create.clicked.connect(self._button_create)

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(lbl_weight, 0, 0)
        grid_layout.addWidget(self.sb_weight, 0, 1)
        grid_layout.addWidget(lbl_length, 1, 0)
        grid_layout.addWidget(self.sb_length, 1, 1)
        grid_layout.addWidget(self.pb_create, 2, 1)

    def set_data(self, data):
        """Creating the data object."""
        self.data = data

    def _button_create(self):
        """Button create.
        Getting the user input from the widgets.
        Creating the new measurement in the database.
        Closing the Dialog.
        """
        weight = self.sb_weight.value()
        length = self.sb_length.value()

        self._create_new_measurement(weight=weight, length=length)

        self.accept()

    def _create_new_measurement(self, weight: int, length: int):
        """Creating a new measurement in the database."""
        tuple_data = namedtuple('m_header', ['h_id', 'u_id', 'h_date', 'h_weight', 'h_length'])

        h_id = len(self.data.old_measurement)
        h_date = str(datetime.datetime.today())[:9]

        self.data.new_measurement = tuple_data(h_id, self.data.user.u_id, h_date, weight, length)

        with open_sqlite3() as cursor:
            cursor.execute('INSERT INTO m_header VALUES (?, ?, ?, ?, ?) ', self.data.new_measurement)
