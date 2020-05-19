# -*- coding: utf-8 -*-

"""Creating the open frame."""

from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
from collections import namedtuple


class FrameOpen(QtWidgets.QFrame):
    """The visual layout of the GUI."""

    def __init__(self, data):
        QtWidgets.QFrame.__init__(self)

        self.data = data

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

    def lw_load_data(self):
        """Loading the data into the list widget."""
        m_header = namedtuple('m_header', ['h_id', 'u_id', 'h_date', 'h_weight'])

        self.data.old_measurement.clear()
        self.list_widget.clear()

        # Database:
        with open_sqlite3() as cursor:
            cursor.execute('SELECT h_id, u_id, h_date, h_weight FROM m_header')
            data = cursor.fetchall()

        for row in data:
            self.data.old_measurement.append(m_header(*row))
            self.list_widget.addItem(f'ID: {row[0]} | Date: {row[2]} | Weight: {row[3]}')

