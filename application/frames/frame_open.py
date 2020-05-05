#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creating the open frame."""

from PyQt5 import QtWidgets


class FrameOpen(QtWidgets.QFrame):
    """The visual layout of the GUI."""

    def __init__(self, font):
        QtWidgets.QFrame.__init__(self)

        self.setFont(font.calibir_12)

        lbl = QtWidgets.QLabel('Open')

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(lbl)
