#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The main application."""

from application import main_window, font, menu, status_bar
from application.frames import frame_home, frame_new, frame_open
from application.dialogs import user_dialog


from PyQt5 import QtWidgets
import sys


class Application(main_window.MainWindow):
    """The main class of the gui."""

    def __init__(self):
        main_window.MainWindow.__init__(self)

        # Dialog:
        dialog_user = user_dialog.UserDialog(self)
        if dialog_user.exec_() != QtWidgets.QDialog.Accepted:
            sys.exit()
        self.user = dialog_user.return_user()

        self.font = font.Fonts()

        self.menu_bar = menu.Menu(font=self.font)
        self.setMenuBar(self.menu_bar)

        self.status_bar = status_bar.Statusbar(font=self.font, user=self.user)
        self.setStatusBar(self.status_bar)

        self.frame_home = frame_home.FrameHome(font=self.font)
        self.frame_new = frame_new.FrameNew(font=self.font)
        self.frame_open = frame_open.FrameOpen(font=self.font)

        self.central_layout.addWidget(self.frame_home)

        # Connect:
        self.connect_widgets()

    def connect_widgets(self):
        """Connecting the widgets of the main window to the methods."""
        self.frame_home.pb_h_open.clicked.connect(self.button_h_open)
        self.frame_home.pb_h_new.clicked.connect(self.button_h_new)

    # Main window:
    def button_h_open(self):
        """Updating the main window and showing the open frame."""
        self.frame_home.hide()
        self.central_layout.removeWidget(self.frame_home)
        self.central_layout.addWidget(self.frame_open)
        self.frame_open.show()

    def button_h_new(self):
        """Updating the main window and showing the new frame."""
        self.frame_home.hide()
        self.central_layout.removeWidget(self.frame_home)
        self.central_layout.addWidget(self.frame_new)
        self.frame_new.show()
