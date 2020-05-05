#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Main Window."""

from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    """The visual layout of the GUI."""
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.setup_main_window()

    def setup_main_window(self):
        """Setting up the main window."""
        self.setWindowTitle('Projekt 04 - Team MM 1')

        # Creating the central widget:
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Creating the main layout:
        self.central_layout = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.central_layout)
