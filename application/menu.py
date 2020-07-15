# -*- coding: utf-8 -*-

"""Creation and implementation of the menu."""


from application.dialogs import pi_dialog, new_user_dialog
from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui
import os
import sys
from collections import namedtuple
import paramiko
import serial


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

        # Pi:
        menu_pi = QtWidgets.QMenu(self)
        menu_pi.setTitle('Raspberry Pi')
        menu_pi.setFont(font)

        self.menu_pi_quick_connect = QtWidgets.QAction('Quick Connect', self)
        self.menu_pi_quick_connect.setShortcutVisibleInContextMenu(True)

        self.menu_pi_new_connection = QtWidgets.QAction('New Connection', self)
        self.menu_pi_new_connection.setShortcutVisibleInContextMenu(True)

        menu_pi.addAction(self.menu_pi_quick_connect)
        menu_pi.addAction(self.menu_pi_new_connection)

        # Nucleo:
        menu_nucleo = QtWidgets.QMenu(self)
        menu_nucleo.setTitle('Nucleo')
        menu_nucleo.setFont(font)

        self.nucleo_com_1 = QtWidgets.QAction('COM 1', self)
        self.nucleo_com_2 = QtWidgets.QAction('COM 2', self)
        self.nucleo_com_3 = QtWidgets.QAction('COM 3', self)
        self.nucleo_com_4 = QtWidgets.QAction('COM 4', self)
        self.nucleo_com_5 = QtWidgets.QAction('COM 5', self)
        self.nucleo_com_6 = QtWidgets.QAction('COM 6', self)

        menu_nucleo.addAction(self.nucleo_com_1)
        menu_nucleo.addAction(self.nucleo_com_2)
        menu_nucleo.addAction(self.nucleo_com_3)
        menu_nucleo.addAction(self.nucleo_com_4)
        menu_nucleo.addAction(self.nucleo_com_5)
        menu_nucleo.addAction(self.nucleo_com_6)

        # User:
        menu_user = QtWidgets.QMenu(self)
        menu_user.setTitle('User')
        menu_user.setFont(font)

        self.user_add = QtWidgets.QAction('Add User', self)
        self.user_add.setShortcutVisibleInContextMenu(True)

        menu_user.addAction(self.user_add)

        # Adding the menus to the menubar:
        self.addMenu(menu_file)
        self.addMenu(menu_tutorial)
        self.addMenu(menu_pi)
        self.addMenu(menu_nucleo)
        self.addMenu(menu_user)

    def _connect_menu(self):
        """Connecting the menu widgets to the methods."""
        self.menu_close.triggered.connect(self._triggered_menu_close)
        self.menu_close.setShortcut(QtGui.QKeySequence('Ctrl+Q'))

        self.menu_getting_started.triggered.connect(self._triggered_menu_getting_started)
        self.menu_getting_started.setShortcut(QtGui.QKeySequence('F1'))

        self.menu_pi_quick_connect.triggered.connect(self._triggered_menu_pi_quick)
        self.menu_pi_quick_connect.setShortcut(QtGui.QKeySequence('F2'))
        self.menu_pi_new_connection.triggered.connect(self._triggered_menu_pi_new)
        self.menu_pi_new_connection.setShortcut(QtGui.QKeySequence('F3'))

        self.nucleo_com_1.triggered.connect(self._triggered_menu_nucleo)
        self.nucleo_com_2.triggered.connect(self._triggered_menu_nucleo)
        self.nucleo_com_3.triggered.connect(self._triggered_menu_nucleo)
        self.nucleo_com_4.triggered.connect(self._triggered_menu_nucleo)
        self.nucleo_com_5.triggered.connect(self._triggered_menu_nucleo)
        self.nucleo_com_6.triggered.connect(self._triggered_menu_nucleo)

        self.nucleo_com_1.setShortcut(QtGui.QKeySequence('Ctrl+1'))
        self.nucleo_com_2.setShortcut(QtGui.QKeySequence('Ctrl+2'))
        self.nucleo_com_3.setShortcut(QtGui.QKeySequence('Ctrl+3'))
        self.nucleo_com_4.setShortcut(QtGui.QKeySequence('Ctrl+4'))
        self.nucleo_com_5.setShortcut(QtGui.QKeySequence('Ctrl+5'))
        self.nucleo_com_6.setShortcut(QtGui.QKeySequence('Ctrl+6'))

        self.user_add.triggered.connect(self._triggered_menu_user_add)
        self.user_add.setShortcut(QtGui.QKeySequence('F4'))

    @staticmethod
    def _triggered_menu_close():
        """Closing the program."""
        sys.exit()

    @staticmethod
    def _triggered_menu_getting_started():
        """Opening the tutorial."""
        os.startfile(fr'{os.curdir}\src\user_documentation\user_documentation.pdf')

    def _triggered_menu_pi_quick(self):
        """Reconnect with last successful connection to Pi.
        Opening the pi.txt file, and testing the connection with the data.
        """
        message = QtWidgets.QMessageBox()
        raspberry_pi = namedtuple('Pi', ['ip', 'port', 'name', 'password'])

        with open(fr'{os.curdir}\src\files\pi.txt') as file:
            text = file.read()
            data = text.split('\n')

        self.data.raspberry_pi = raspberry_pi(*data)

        if self._connect_pi():
            self.main_window.status_bar.lbl_pi.setText(f'Pi: {self.data.raspberry_pi.ip}')
            message.information(self, 'Information', f'Connected to: {self.data.raspberry_pi.ip}')

        else:
            self.data.raspberry_pi = None
            message.warning(self, 'Warning', 'No connection to the Raspberry Pi!')

    def _triggered_menu_pi_new(self):
        """Testing the connection to the pi.
        First the dialog is opened, then the user is notified if the connection was successful or not.
        """
        message = QtWidgets.QMessageBox()

        dialog_pi = pi_dialog.PiConnection(self)
        dialog_pi.set_data(data=self.data)
        if dialog_pi.exec_() != QtWidgets.QDialog.Accepted:
            message.warning(self, 'Warning', 'Connection Failed!')
        del dialog_pi

        if self._connect_pi():
            message.information(self, 'Information', 'Connection Successful!')
            with open('src/files/pi.txt', 'w') as file:
                file.write(f'{self.data.raspberry_pi.ip}\n'
                           f'{self.data.raspberry_pi.port}\n'
                           f'{self.data.raspberry_pi.name}\n'
                           f'{self.data.raspberry_pi.password}')

        else:
            message.warning(self, 'Warning', 'Connection Failed!')

    def _connect_pi(self) -> bool:
        """Connect to Pi and setup.
        The connection to the Raspberry Pi is tested. Also the pigpiod is set to the Pi (Enables the GPIO control over
        the SSH connection). If the connection fails, a message box is displayed.
        """
        try:
            cmd = 'sudo pigpiod'

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.data.raspberry_pi.ip, self.data.raspberry_pi.port,
                        self.data.raspberry_pi.name, self.data.raspberry_pi.password)
            ssh.exec_command(cmd)
            return True

        except:
            return False

    def _triggered_menu_nucleo(self):
        """Testing the connection to the Nucleo.
        First the widget that sent the signal is verified. The connection to the Nucleo is tested accordingly.
        The user is then notified whether the connection was successful or not.
        """
        sender = self.sender()
        port = 'COM'
        if sender == self.nucleo_com_1:
            port += '1'
        elif sender == self.nucleo_com_2:
            port += '2'
        elif sender == self.nucleo_com_3:
            port += '3'
        elif sender == self.nucleo_com_4:
            port += '4'
        elif sender == self.nucleo_com_5:
            port += '5'
        elif sender == self.nucleo_com_6:
            port += '6'
        else:
            raise ValueError('A new method is referring to this method.')

        self.data.nucleo = port

        self._test_nucleo()

    def _test_nucleo(self):
        """Testing the connection to the Nucleo.
        Test the connection with the Nucleo to the designated COM port.
        """
        message = QtWidgets.QMessageBox()
        try:
            connection = serial.Serial(self.data.nucleo, 115200, timeout=2)
            connection.close()

        except serial.serialutil.SerialException:
            message.warning(self, 'Warning', 'Connection Failed!')
            self.data.nucleo = None
            return

        message.information(self, 'Information', 'Connection Successful!')
        self.main_window.status_bar.lbl_nucleo.setText(f'Nucleo: {self.data.nucleo}')

    def _triggered_menu_user_add(self):
        """Adding a user to the database.
        Creating the new user dialog.
        """
        message = QtWidgets.QMessageBox()

        dialog_new_user = new_user_dialog.NewUserDialog(self)
        dialog_new_user.set_data(data=self.data)
        if dialog_new_user.exec_() != QtWidgets.QDialog.Accepted:
            message.warning(self, 'Warning', 'No user was created!')
        else:
            message.information(self, 'Warning', 'User was successfully created!')

        del dialog_new_user
