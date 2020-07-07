#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creation and implementation of the menu."""

from PyQt5 import QtWidgets, QtGui


class Statusbar(QtWidgets.QStatusBar):
    """The main class of the menu."""

    def __init__(self, data):
        QtWidgets.QStatusBar.__init__(self)

        self.setFont(QtGui.QFont('Calibri', 12))

        self.lbl_version = QtWidgets.QLabel('  Version: 1.0  ')
        self.addPermanentWidget(self.lbl_version)

        self.lbl_user = QtWidgets.QLabel(f'  {data.user.u_name}  ')
        self.addPermanentWidget(self.lbl_user)

        self.lbl_pi = QtWidgets.QLabel('  Pi-IP: Not Connected  ')
        self.addPermanentWidget(self.lbl_pi)

        self.lbl_nucleo = QtWidgets.QLabel('  Nucleo: Not Connected  ')
        self.addPermanentWidget(self.lbl_nucleo)
