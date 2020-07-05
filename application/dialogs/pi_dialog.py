# -*- coding: utf-8 -*-

"""Dialog to create a new measurement."""

from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
from collections import namedtuple
import datetime


class PiConnection(QtWidgets.QDialog):
    """Dialog - new measurement."""
    def __init__(self, *args, **kwargs):
        super(PiConnection, self).__init__(*args, **kwargs)

        self.data = None
        self._create_widgets()

    def _create_widgets(self):
        """Creating the widgets."""
        self.setWindowTitle('Connect to Raspberry Pi')
        self.setFont(QtGui.QFont('Calibri', 12))

        lbl_ip = QtWidgets.QLabel('IP-Address: ')
        self.le_ip = QtWidgets.QLineEdit()

        lbl_port = QtWidgets.QLabel('Port: ')
        self.sb_port = QtWidgets.QSpinBox()
        self.sb_port.setValue(22)

        lbl_name = QtWidgets.QLabel('Name: ')
        self.le_name = QtWidgets.QLineEdit()

        lbl_password = QtWidgets.QLabel('Password: ')
        self.le_password = QtWidgets.QLineEdit()

        self.pb_test = QtWidgets.QPushButton('Test Connection')
        self.pb_test.clicked.connect(self._button_test)

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(lbl_ip, 0, 0)
        grid_layout.addWidget(self.le_ip, 0, 1)
        grid_layout.addWidget(lbl_port, 1, 0)
        grid_layout.addWidget(self.sb_port, 1, 1)
        grid_layout.addWidget(lbl_name, 2, 0)
        grid_layout.addWidget(self.le_name, 2, 1)
        grid_layout.addWidget(lbl_password, 3, 0)
        grid_layout.addWidget(self.le_password, 3, 1)
        grid_layout.addWidget(self.pb_test, 4, 1)

    def set_data(self, data):
        """Creating the data object."""
        self.data = data

    def _button_test(self):
        """"""
        # TODO testing the connection and updating the file
        ip = self.le_ip.text()
        port = self.sb_port.value()
        name = self.le_name.text()
        password = self.le_password.text()

        print(ip, port, name, password)
