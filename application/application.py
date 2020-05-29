# -*- coding: utf-8 -*-

"""The main application."""

from application import main_window, menu, status_bar, data
from application.frames import frame_sidebar, frame_new, frame_open, frame_plot
from application.dialogs import user_dialog, new_measurement_dialog


from PyQt5 import QtWidgets
import sys


class Application(main_window.MainWindow):
    """The main class of the gui."""

    def __init__(self):
        main_window.MainWindow.__init__(self)

        self.data = data.Data()

        # Dialog:
        dialog_user = user_dialog.UserDialog(self)
        dialog_user.set_data(data=self.data)
        if dialog_user.exec_() != QtWidgets.QDialog.Accepted:
            sys.exit()
        del dialog_user

        # Menu:
        self.menu_bar = menu.Menu()
        self.setMenuBar(self.menu_bar)

        # Statusbar:
        self.status_bar = status_bar.Statusbar(data=self.data)
        self.setStatusBar(self.status_bar)

        self.frame_sidebar = frame_sidebar.FrameSidebar()
        self.frame_new = frame_new.FrameNew(data=self.data)
        self.frame_open = frame_open.FrameOpen(data=self.data, main_window=self)
        self.frame_plot = frame_plot.FramePlot(data=self.data)

        self.central_layout.addWidget(self.frame_sidebar, 2, 0)  # Adding the frame to the main window

        self._connect_methods()

    def _connect_methods(self):
        """Connecting the widgets of the main window to the methods."""
        self.frame_sidebar.pb_h_open.clicked.connect(self._button_h_open)
        self.frame_sidebar.pb_h_new.clicked.connect(self._button_h_new)

    def _button_h_open(self):
        """Updating the main window and showing the open frame."""
        self.central_layout.removeWidget(self.frame_new)
        self.frame_new.hide()

        self.central_layout.addWidget(self.frame_open, 2, 2, 1, 2)
        self.frame_open.show()
        self.lbl_header.setText('Open Measurement')

        self.frame_open.lw_load_data()

    def _button_h_new(self):
        """Updating the main window and showing the new frame."""
        self.central_layout.removeWidget(self.frame_open)
        self.frame_open.hide()

        self.central_layout.addWidget(self.frame_new, 2, 2, 1, 2)
        self.frame_new.show()
        self.lbl_header.setText('New Measurement')

        dialog = new_measurement_dialog.NewMeasurement()
        dialog.set_data(data=self.data)
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return
        del dialog

        self.frame_new.update_widgets()



