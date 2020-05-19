#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creating the new frame."""

from PyQt5 import QtWidgets, QtGui


class FrameNew(QtWidgets.QFrame):
    """The visual layout of the GUI."""
    def __init__(self):
        QtWidgets.QFrame.__init__(self)

        self.setFont(QtGui.QFont('Calibri', 12))

        lbl = QtWidgets.QLabel('New')

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(lbl)

