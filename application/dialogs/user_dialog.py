# -*- coding: utf-8 -*-

"""Widgets for the main window."""

from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
import collections


class UserDialog(QtWidgets.QDialog):
    """The visual layout of the GUI."""
    def __init__(self, *args, **kwargs):
        super(UserDialog, self).__init__(*args, **kwargs)

        # User data:
        self.user_data = []
        self.data = None

        self._create_widgets()

    def _create_widgets(self):
        """Creating the widgets."""
        self.setWindowTitle('Select User')
        self.setFont(QtGui.QFont('Calibri', 12))

        lbl_user = QtWidgets.QLabel('User:')
        self.cb_user = QtWidgets.QComboBox()
        self._add_items()

        self.pb_start = QtWidgets.QPushButton()
        self.pb_start.setText('Start')
        self.pb_start.clicked.connect(self._button_start)

        self.pb_exit = QtWidgets.QPushButton()
        self.pb_exit.setText('Exit')
        self.pb_exit.clicked.connect(self._button_exit)

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(lbl_user, 0, 0)
        grid_layout.addWidget(self.cb_user, 0, 1)
        grid_layout.addWidget(self.pb_start, 1, 1)
        grid_layout.addWidget(self.pb_exit, 2, 1)

    def set_data(self, data):
        """Creating the data object."""
        self.data = data

    def _add_items(self):
        """Adding items to the combo box."""
        n_tuple = collections.namedtuple('user_data', ['u_id', 'u_name', 'u_email'])

        # Database:
        with open_sqlite3() as cursor:
            cursor.execute('SELECT u_id, u_name, u_email FROM m_user')
            data = cursor.fetchall()

        for row in data:
            self.cb_user.addItem(row[1])
            self.user_data.append(n_tuple(*row))

    def _button_start(self):
        """Starting the program."""
        index = self.cb_user.currentIndex()
        self.data.user = self.user_data[index]

        self.accept()

    def _button_exit(self):
        """Closing the program."""
        self.reject()
