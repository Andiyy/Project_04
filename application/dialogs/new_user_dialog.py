# -*- coding: utf-8 -*-

"""Dialog to chose witch user is testing."""


from database.database import open_sqlite3

from PyQt5 import QtWidgets, QtGui


class NewUserDialog(QtWidgets.QDialog):
    """Dialog - User."""
    def __init__(self, *args, **kwargs):
        super(NewUserDialog, self).__init__(*args, **kwargs)

        # User data:
        self.user_data = []
        self.data = None

        self.name = None
        self.email = None

        self._create_widgets()

    def _create_widgets(self):
        """Creating the widgets."""
        self.setWindowTitle('Create New User')
        self.setFont(QtGui.QFont('Calibri', 12))

        lbl_name = QtWidgets.QLabel('Name: ')
        self.le_name = QtWidgets.QLineEdit()

        lbl_email = QtWidgets.QLabel('Email: ')
        self.le_email = QtWidgets.QLineEdit()
        self.le_email.setText('@hs-augsburg.de')

        self.pb_create = QtWidgets.QPushButton('Create User')
        self.pb_create.clicked.connect(self._button_create)

        grid_layout = QtWidgets.QGridLayout(self)
        grid_layout.addWidget(lbl_name, 0, 0)
        grid_layout.addWidget(self.le_name, 0, 1)
        grid_layout.addWidget(lbl_email, 1, 0)
        grid_layout.addWidget(self.le_email, 1, 1)
        grid_layout.addWidget(self.pb_create, 2, 1)

    def set_data(self, data):
        """Creating the data object."""
        self.data = data

    def _button_create(self):
        """Button create new user.
        First the user inputs are read in and checked. If they are incorrect, an error message is displayed.
        If the data is ok, a new entry is created in the database. At last the dialog is closed.
        """
        message = QtWidgets.QMessageBox()

        self.name = self.le_name.text().strip()
        self.email = self.le_email.text().strip()

        if self.name == '' or self.email == '' or '@hs-augsburg.de' not in self.email or len(self.email) < 16:
            message.warning(self, 'Warning', 'The name/email is invalid!')
            return

        self._create_new_user()

        self.accept()

    def _create_new_user(self):
        """Creating a new user in the database.
        First it is calculated how many entries are in the database.
        Then a new entry is created in the database with the corresponding data.
        """
        amount_user = 1

        with open_sqlite3() as cursor:
            cursor.execute('SELECT u_id FROM m_user')
            data = cursor.fetchall()

        for _ in data:
            amount_user += 1

        with open_sqlite3() as cursor:
            cursor.execute('INSERT INTO m_user VALUES (?, ?, ?) ', [amount_user, self.name, self.email])
