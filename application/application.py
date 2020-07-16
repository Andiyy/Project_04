# -*- coding: utf-8 -*-

"""The main application."""

from application import main_window, menu, status_bar, data
from application.frames import frame_sidebar, frame_new, frame_open
from application.dialogs import user_dialog, new_measurement_dialog


from PyQt5 import QtWidgets, QtGui
import sys


class Application(main_window.MainWindow):
    """The main class of the gui."""

    def __init__(self):
        main_window.MainWindow.__init__(self)

        self.data = data.Data()

        self._user_dialog()

        # Menu:
        self.menu_bar = menu.Menu(data=self.data, main_window=self)
        self.setMenuBar(self.menu_bar)

        # Statusbar:
        self.status_bar = status_bar.Statusbar(data=self.data)
        self.setStatusBar(self.status_bar)

        # Frames:
        self.frame_sidebar = frame_sidebar.FrameSidebar()
        self.frame_new = frame_new.FrameNew(data=self.data, main_window=self)
        self.frame_open = frame_open.FrameOpen(data=self.data, main_window=self)

        self.central_layout.addWidget(self.frame_sidebar, 2, 0)  # Adding the frame to the main window

        self._connect_methods()

    def _user_dialog(self):
        """Creating the user dialog.
        If the dialog was accepted the program starts. If not, the program is closed.
        """
        dialog_user = user_dialog.UserDialog(self)
        dialog_user.set_data(data=self.data)
        if dialog_user.exec_() != QtWidgets.QDialog.Accepted:
            sys.exit()
        del dialog_user

    def _connect_methods(self):
        """Connecting the widgets of the main window to the methods."""
        self.frame_sidebar.pb_h_open.clicked.connect(self._button_h_open)
        self.frame_sidebar.pb_h_open.setShortcut(QtGui.QKeySequence('Ctrl+O'))
        self.frame_sidebar.pb_h_new.clicked.connect(self._button_h_new)
        self.frame_sidebar.pb_h_new.setShortcut(QtGui.QKeySequence('Ctrl+N'))

    def _button_h_open(self):
        """Updating the main window and showing the open frame."""
        self.central_layout.removeWidget(self.frame_new)
        self.frame_new.hide()

        self.central_layout.addWidget(self.frame_open, 2, 2, 1, 2)
        self.frame_open.show()
        self.lbl_header.setText('Open Measurement')

        self.frame_open.lw_load_data()

    def _button_h_new(self):
        """Updating the main window and showing the new frame.
        If no connection is established to the devices, an error message is displayed.
        """
        message = QtWidgets.QMessageBox()
        if not self.data.raspberry_pi:
            message.warning(self, 'Warning', 'First a connection to Raspberry Pi must be created.')
            return
        elif not self.data.nucleo:
            message.warning(self, 'Warning', 'First a connection to Nucleo must be created.')
            return

        self.frame_open.lw_load_data()

        # Creating the NewMeasurement dialog:
        dialog = new_measurement_dialog.NewMeasurement()
        dialog.set_data(data=self.data)
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return
        del dialog

        # Updating the main window:
        self.central_layout.removeWidget(self.frame_open)
        self.frame_open.hide()

        self.central_layout.addWidget(self.frame_new, 2, 2, 1, 2)
        self.frame_new.show()
        self.lbl_header.setText('New Measurement')

        self.frame_new.update_widgets()
