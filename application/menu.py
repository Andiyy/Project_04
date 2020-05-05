#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creation and implementation of the menu."""


from PyQt5 import QtWidgets, QtGui
import os
import sys


class Menu(QtWidgets.QMenuBar):
    """The main class of the menu."""
    def __init__(self, font):
        QtWidgets.QMenuBar.__init__(self)

        self.font = font

        self.create_widgets()
        self.connect_menu()

    def create_widgets(self):
        """Creating the widgets."""
        self.setFont(self.font.calibir_12)

        # Settings:
        menu_file = QtWidgets.QMenu(self)
        menu_file.setTitle('File')
        menu_file.setFont(self.font.calibir_12)

        self.menu_close = QtWidgets.QAction('Close', self)
        self.menu_close.setShortcutVisibleInContextMenu(True)

        menu_file.addAction(self.menu_close)

        # Tutorial:
        menu_tutorial = QtWidgets.QMenu(self)
        menu_tutorial.setTitle('Tutorial')
        menu_tutorial.setFont(self.font.calibir_12)

        self.menu_getting_started = QtWidgets.QAction('Getting Started', self)
        self.menu_getting_started.setShortcutVisibleInContextMenu(True)

        menu_tutorial.addAction(self.menu_getting_started)

        # Adding the menus to the menubar:
        self.addMenu(menu_file)
        self.addMenu(menu_tutorial)

    def connect_menu(self):
        """Connecting the menu widgets to the methods."""
        self.menu_close.triggered.connect(self.triggered_menu_close)
        self.menu_close.setShortcut(QtGui.QKeySequence('Ctrl+Q'))

        self.menu_getting_started.triggered.connect(self.triggered_menu_getting_started)
        self.menu_getting_started.setShortcut(QtGui.QKeySequence('F1'))

    @staticmethod
    def triggered_menu_close():
        """Closing the program."""
        sys.exit()

    @staticmethod
    def triggered_menu_getting_started():
        """Opening the tutorial."""
        os.startfile(fr'{os.curdir}\application\files\user_documentation\user_documentation.pdf')
