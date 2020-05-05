#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creating the new frame."""

from PyQt5 import QtWidgets


class FrameNew(QtWidgets.QFrame):
    """The visual layout of the GUI."""
    def __init__(self, font):
        QtWidgets.QFrame.__init__(self)

        self.setFont(font.calibir_12)

        lbl = QtWidgets.QLabel('New')

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(lbl)

    def new_measurement(self):
        """Creating a new measurement in the database."""

