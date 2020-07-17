#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Showing different plots."""

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

from database.database import open_sqlite3

matplotlib.rcParams.update({'font.size': 25})


def plot_data(x: np.array, array_1: np.array, title_lbl: str, x_lbl: str, y_lbl: str, color: str):
    """Plotting the data.

    :param x:           X-Values (Time)
    :param array_1:     Y-Values
    :param title_lbl:   Title
    :param x_lbl:       X label (Time)
    :param y_lbl:       Y label (Power or Torque)
    :param color:       Color
    """

    fig, ax = plt.subplots()

    fig.dpi = 100

    ax.plot(x, array_1, '-*', color=color)
    ax.set_title(title_lbl)
    ax.set_xlabel(x_lbl, )
    ax.set_ylabel(y_lbl)
    ax.grid()
    plt.show()

    name = str(time.time())
    fig.savefig(f'{name.replace(".", "_")}.png', transparent=True)


def get_data(array: np.array, h_id: int, s_id: int):
    """Getting the data from the database and soring it into the array.

    :param array:   The array where the measurement data are stored.
    :param h_id:    Measurement id
    :param s_id:    Sensor id
    """
    with open_sqlite3() as cursor:
        cursor.execute('SELECT d_value FROM m_data WHERE h_id=? AND s_id=?',
                       (h_id, s_id))
        data = cursor.fetchall()

    for line, row in enumerate(data):
        array[line] = row[0]


# PLOT 4kg

x_time = np.arange(0, 9, 0.01)
y_current = np.zeros(900)
y_voltage = np.zeros(900)
y_power = np.zeros(900)

get_data(y_current, 8, 1)
plot_data(x_time, y_current, "Current - 4kg", "Time in s", "Current in A", 'r')

get_data(y_voltage, 8, 2)
plot_data(x_time, y_voltage, "Voltage - 4kg", "Time in s", "Voltage in V", 'b')

for i in range(len(y_power)):
    y_power[i] = y_current[i] * y_voltage[i]

plot_data(x_time, y_power, "Power - 4kg", "Time in s", "Power in W", 'g')


x_time_rpm = np.arange(0, 9, 0.5)
y_rpm = np.zeros(18)

get_data(y_rpm, 8, 3)
plot_data(x_time_rpm, y_rpm, "RPM - 4kg", "Time in s", "RPM in 1/min", 'm')

# Average Current and average Torque
i = [0, 3.9473033016154977, 4.103951623183526, 4.362873194273027, 4.5223836863946065, 4.658608200413441]
t = [0, 4.5973951900116825, 4.947066836537942, 5.339683593606451, 5.664413282928584, 7.083524043516428]

plot_data(t, i, 'Performance Characteristics Curve', 'Torque in Nm', 'Current in A', 'c')
