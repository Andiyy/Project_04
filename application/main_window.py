# -*- coding: utf-8 -*-

"""Main Window."""

from PyQt5 import QtWidgets, QtGui


class MainWindow(QtWidgets.QMainWindow):
    """The visual layout of the GUI."""
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self._setup_main_window()

    def _setup_main_window(self):
        """Setting up the main window."""
        self.setWindowTitle('Projekt 04 - Team MM 1')

        # Creating the central widget:
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        # Creating the main layout:
        self.central_layout = QtWidgets.QGridLayout()
        self.central_widget.setLayout(self.central_layout)

        self.lbl_header = QtWidgets.QLabel()
        self.lbl_header.setText('Home')
        self.lbl_header.setFont(QtGui.QFont('Calibri', 16, QtGui.QFont.Bold))

        self.line_horizontal = QtWidgets.QFrame()
        self.line_horizontal.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_horizontal.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.line_vertical = QtWidgets.QFrame()
        self.line_vertical.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_vertical.setFrameShadow(QtWidgets.QFrame.Sunken)

        spacer = QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        self.central_layout.addWidget(self.lbl_header, 0, 2)
        self.central_layout.addWidget(self.line_horizontal, 1, 0, 1, 4)
        self.central_layout.addWidget(self.line_vertical, 0, 1, 4, 1)
        self.central_layout.addItem(spacer, 0, 3)
