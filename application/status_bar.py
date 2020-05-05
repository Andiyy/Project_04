#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creation and implementation of the menu."""

from PyQt5 import QtWidgets


class Statusbar(QtWidgets.QStatusBar):
    """The main class of the menu."""

    def __init__(self, font, user):
        QtWidgets.QStatusBar.__init__(self)

        self.setFont(font.calibir_12)

        self.lbl_user = QtWidgets.QLabel(user.u_name)
        self.addPermanentWidget(self.lbl_user)
