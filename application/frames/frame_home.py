#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creating the home frame."""

from PyQt5 import QtWidgets


class FrameHome(QtWidgets.QFrame):
    """The visual layout of the GUI."""
    def __init__(self, font):
        QtWidgets.QFrame.__init__(self)

        self.setFont(font.calibir_12)

        self.pb_h_new = QtWidgets.QPushButton()
        self.pb_h_new.setText('New')

        self.pb_h_open = QtWidgets.QPushButton()
        self.pb_h_open.setText('Open')

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(self.pb_h_new, 0, 0)
        grid_layout.addWidget(self.pb_h_open, 0, 1)


