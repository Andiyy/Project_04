#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creating the home frame."""

from PyQt5 import QtWidgets, QtGui


class FrameSidebar(QtWidgets.QFrame):
    """The visual layout of the GUI."""
    def __init__(self):
        QtWidgets.QFrame.__init__(self)

        self.setFont(QtGui.QFont('Calibri', 12))

        self.pb_h_new = QtWidgets.QPushButton()
        self.pb_h_new.setText('New Measurement')

        self.pb_h_open = QtWidgets.QPushButton()
        self.pb_h_open.setText('Open Measurement')

        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(self.pb_h_new)
        grid_layout.addWidget(self.pb_h_open)
        grid_layout.addItem(spacer)


