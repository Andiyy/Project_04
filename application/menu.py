#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Creation and implementation of the menu."""


from PyQt5 import QtWidgets, QtGui
import os
import sys
from collections import namedtuple
import paramiko


class Menu(QtWidgets.QMenuBar):
    """The main class of the menu."""
    def __init__(self, data, main_window):
        QtWidgets.QMenuBar.__init__(self)

        self.data = data
        self.main_window = main_window

        self._create_widgets()
        self._connect_menu()

    def _create_widgets(self):
        """Creating the widgets."""
        font = QtGui.QFont('Calibri', 12)

        self.setFont(font)

        # Settings:
        menu_file = QtWidgets.QMenu(self)
        menu_file.setTitle('File')
        menu_file.setFont(font)

        self.menu_close = QtWidgets.QAction('Close', self)
        self.menu_close.setShortcutVisibleInContextMenu(True)

        menu_file.addAction(self.menu_close)

        # Tutorial:
        menu_tutorial = QtWidgets.QMenu(self)
        menu_tutorial.setTitle('Tutorial')
        menu_tutorial.setFont(font)

        self.menu_getting_started = QtWidgets.QAction('Getting Started', self)
        self.menu_getting_started.setShortcutVisibleInContextMenu(True)

        menu_tutorial.addAction(self.menu_getting_started)

        # Pi
        menu_pi = QtWidgets.QMenu(self)
        menu_pi.setTitle('Raspberry Pi')
        menu_pi.setFont(font)

        self.menu_pi_quick_connect = QtWidgets.QAction('Quick Connect', self)
        self.menu_pi_quick_connect.setShortcutVisibleInContextMenu(True)

        self.menu_pi_new_connection = QtWidgets.QAction('New Connection', self)
        self.menu_pi_new_connection.setShortcutVisibleInContextMenu(True)

        menu_pi.addAction(self.menu_pi_quick_connect)
        menu_pi.addAction(self.menu_pi_new_connection)

        # Nukleo:
        menu_nukleo = QtWidgets.QMenu(self)
        menu_nukleo.setTitle('Nukleo')
        menu_nukleo.setFont(font)

        self.nukleo_com_1 = QtWidgets.QAction('COM 1', self)
        self.nukleo_com_2 = QtWidgets.QAction('COM 2', self)
        self.nukleo_com_3 = QtWidgets.QAction('COM 3', self)
        self.nukleo_com_4 = QtWidgets.QAction('COM 4', self)
        self.nukleo_com_5 = QtWidgets.QAction('COM 5', self)
        self.nukleo_com_6 = QtWidgets.QAction('COM 6', self)

        menu_nukleo.addAction(self.nukleo_com_1)
        menu_nukleo.addAction(self.nukleo_com_2)
        menu_nukleo.addAction(self.nukleo_com_3)
        menu_nukleo.addAction(self.nukleo_com_4)
        menu_nukleo.addAction(self.nukleo_com_5)
        menu_nukleo.addAction(self.nukleo_com_6)

        # Adding the menus to the menubar:
        self.addMenu(menu_file)
        self.addMenu(menu_tutorial)
        self.addMenu(menu_pi)
        self.addMenu(menu_nukleo)

    def _connect_menu(self):
        """Connecting the menu widgets to the methods."""
        self.menu_close.triggered.connect(self._triggered_menu_close)
        self.menu_close.setShortcut(QtGui.QKeySequence('Ctrl+Q'))

        self.menu_getting_started.triggered.connect(self._triggered_menu_getting_started)
        self.menu_getting_started.setShortcut(QtGui.QKeySequence('F1'))

        self.menu_pi_quick_connect.triggered.connect(self._triggered_menu_pi_quick)
        self.menu_pi_new_connection.triggered.connect(self._triggered_menu_pi_new)

        self.nukleo_com_1.triggered.connect(self._triggered_menu_nukleo)
        self.nukleo_com_2.triggered.connect(self._triggered_menu_nukleo)
        self.nukleo_com_3.triggered.connect(self._triggered_menu_nukleo)
        self.nukleo_com_4.triggered.connect(self._triggered_menu_nukleo)
        self.nukleo_com_5.triggered.connect(self._triggered_menu_nukleo)
        self.nukleo_com_6.triggered.connect(self._triggered_menu_nukleo)

    @staticmethod
    def _triggered_menu_close():
        """Closing the program."""
        sys.exit()

    @staticmethod
    def _triggered_menu_getting_started():
        """Opening the tutorial."""
        os.startfile(fr'{os.curdir}\application\files\user_documentation\user_documentation.pdf')

    def _triggered_menu_pi_quick(self):
        """"""
        raspberry_pi = namedtuple('Pi', ['ip', 'port', 'name', 'password'])

        with open(fr'{os.curdir}\src\files\pi.txt') as file:
            text = file.read()
            data = text.split('\n')

        self.data.raspberry_pi = raspberry_pi(*data)

        self._connect_pi()

        self.main_window.status_bar.lbl_pi.setText(f'Pi: {self.data.raspberry_pi.ip}')

        message = QtWidgets.QMessageBox()
        message.information(self, 'Information', f'Connected to: {self.data.raspberry_pi.ip}')

    def _triggered_menu_pi_new(self):
        """"""
        # TODO: Opening a new dialog

    def _triggered_menu_nukleo(self):
        """"""
        sender = self.sender()
        port = 'COM'
        if sender == self.nukleo_com_1:
            port += '1'
        elif sender == self.nukleo_com_2:
            port += '2'
        elif sender == self.nukleo_com_3:
            port += '3'
        elif sender == self.nukleo_com_4:
            port += '4'
        elif sender == self.nukleo_com_5:
            port += '65'
        elif sender == self.nukleo_com_6:
            port += '6'
        else:
            raise ValueError('A new method is referring to this method.')

        self.data.nukleo = port

        self._test_nukleo()

    def _test_nukleo(self):
        """Testing the connection to the Nukleo."""
        message = QtWidgets.QMessageBox()
        # TODO test the connection
        try:
            pass
        except:
            message.warning(self, 'Warning', 'Connection Failed!')
            return

        message.information(self, 'Information', 'Connection Successful!')
        self.main_window.status_bar.lbl_nukleo.setText(f'Nukleo: {self.data.nukleo}')

    def _connect_pi(self):
        """Connect to Pi and setup.
        The connection to the Raspberry Pi is tested. Also the pigpiod is set to the Pi (Enables the GPIO control over
        the SSH connection. If the connection fails, a message box is displayed.
        """
        # TODO Test what happens if the pi is off or the connection is false.
        try:
            cmd = 'sudo pigpiod'

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.data.raspberry_pi.ip, self.data.raspberry_pi.port,
                        self.data.raspberry_pi.name, self.data.raspberry_pi.password)
            ssh.exec_command(cmd)

        except TimeoutError:
            message = QtWidgets.QMessageBox()
            message.warning(self, 'Warning', 'No connection to the Raspberry Pi!')
