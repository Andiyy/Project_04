# -*- coding: utf-8 -*-

""""""

from database.database import open_sqlite3

import time
import random
import numpy as np


class RunProgram:
    """"""

    def __init__(self, data):
        self.data = data

        # Time/Steps:
        self._amount_steps = int(5 / self.data.new_measurement.h_step + 1)
        self._current_step = 0
        # Creating the arrays:

        self._y_voltage = np.zeros(self._amount_steps)
        self._y_current = np.zeros(self._amount_steps)
        self._x_time = np.arange(0, 5.001, self.data.new_measurement.h_step)

        self.data.measured_values = {'Voltage': self._y_voltage, 'Current': self._y_current, 'Time': self._x_time}

    def start(self):
        """Running the Program"""
        for current_step in range(self._amount_steps):
            # Current:
            current = random.random()
            self._y_current[current_step] = current

            # Voltage:
            voltage = random.random()
            self._y_voltage[current_step] = voltage

            time.sleep(self.data.new_measurement.h_step)

        self._write_data()

    def _write_data(self):
        """Writing the data into the database."""
        with open_sqlite3() as cursor:
            for value in self.data.measured_values['Current']:
                cursor.execute('INSERT INTO m_data VALUES (?, ?, ?);',
                               (self.data.new_measurement.h_id, 1, value))

        with open_sqlite3() as cursor:
            for value in self.data.measured_values['Voltage']:
                cursor.execute('INSERT INTO m_data VALUES (?, ?, ?);',
                               (self.data.new_measurement.h_id, 2, value))

        # with open_sqlite3() as cursor:
            # cursor.execute('INSERT INTO m_data VALUES (?, ?, ?);',
            #                (self.data.new_measurement.h_id, 3, self.data.measured_values['Current']))
