#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Showing the 0kg, 2.5kg and 5kg power and torque in a diagram."""

import time
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from database.database import open_sqlite3

x_time = np.arange(0, 9, 0.01)

current_1 = np.zeros(900)
voltage_1 = np.zeros(900)
power_1 = np.zeros(900)

current_2 = np.zeros(900)
voltage_2 = np.zeros(900)
power_2 = np.zeros(900)

current_3 = np.zeros(900)
voltage_3 = np.zeros(900)
power_3 = np.zeros(900)


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


get_data(current_1, 1, 1)
get_data(current_2, 5, 1)
get_data(current_3, 10, 1)

get_data(voltage_1, 1, 2)
get_data(voltage_2, 5, 2)
get_data(voltage_3, 10, 2)


# CALCULATING THE POWER:

def calculate_power(array_current, array_voltage, array_power):
    """Calculate the power.

    :param array_current:   Array with the current data stored.
    :param array_voltage:   Array with the voltage data stored.
    :param array_power:     Array where the performance data should be stored.

    Power = Current * Voltage
    """
    for index in range(len(array_power)):
        array_power[index] = array_current[index] * array_voltage[index]


calculate_power(current_1, voltage_1, power_1)
calculate_power(current_2, voltage_2, power_2)
calculate_power(current_3, voltage_3, power_3)


# CALCULATING THE TORQUE:

time_2 = np.arange(0, 9, 0.5)

rpm_1 = np.zeros(18)
rpm_2 = np.zeros(18)
rpm_3 = np.zeros(18)

power_average_1 = np.zeros(18)
power_average_2 = np.zeros(18)
power_average_3 = np.zeros(18)

torque_1 = np.zeros(18)
torque_2 = np.zeros(18)
torque_3 = np.zeros(18)

get_data(rpm_1, 1, 3)
get_data(rpm_2, 5, 3)
get_data(rpm_3, 10, 3)


def calculate_average_power(array_average: np.array, array_normal: np.array):
    """Calculating the average power.

    :param array_average:   Array where the average performance data should be stored.
    :param array_normal:    Array where the performance data is stored.

    Calculating every 0.5 seconds the average Power.
    """
    reset_counter = np.arange(0, len(power_1), 50)

    counter = 0                                         # Here is the powered added
    counter_1 = 0                                       # Counter

    for index, item in enumerate(array_normal):
        counter += item
        if index in reset_counter:
            counter /= 50
            array_average[counter_1] = counter
            counter = 0                                 # resetting the counter
            counter_1 += 1


calculate_average_power(power_average_1, power_1)
calculate_average_power(power_average_2, power_2)
calculate_average_power(power_average_3, power_3)


def calculate_torque(array_torque: np.array, array_power: np.array, array_rpm: np.array):
    """Calculating the torque.

    :param array_torque:    Array in which the average torques should be stored.
    :param array_power:     Array in which the average power is stored.
    :param array_rpm:       Array in which the average rpm is stored.

    M=P*9.55/n
    """
    for i in range(len(array_torque)):
        if array_rpm[i] != 0:
            array_torque[i] = (array_power[i]*9.55) / array_rpm[i]
        else:
            array_torque[i] = 0


calculate_torque(torque_1, power_average_1, rpm_1)
calculate_torque(torque_2, power_average_2, rpm_2)
calculate_torque(torque_3, power_average_3, rpm_3)


# PLOTTING THE DATA:

def plot_data(x: np.array, array_1: np.array, array_2: np.array, array_3: np.array, lbl_1: str, lbl_2: str):
    """Plotting the data.

    :param x:           X-Values (Time)
    :param array_1:     Y-Values 0kg
    :param array_2:     Y-Values 2.5kg
    :param array_3:     Y-Values 5kg
    :param lbl_1:       X label (Time)
    :param lbl_2:       Y label (Power or Torque)
    """
    fig, ax = plt.subplots()

    fig.dpi = 100

    sns.set_style('whitegrid')

    ax.plot(x, array_1)
    ax.plot(x, array_2)
    ax.plot(x, array_3)

    ax.set_xlabel(lbl_1)
    ax.set_ylabel(lbl_2)

    plt.legend(['0kg', '2.5kg', '5kg'], loc=1)

    ax.grid()
    plt.show()

    name = str(time.time())

    fig.savefig(f'{name.replace(".", "_")}.png', transparent=True)


plot_data(x_time, power_1, power_2, power_3, 'Time in s', 'Power in W')
plot_data(time_2, torque_1, torque_2, torque_3, 'Time in s', 'Torque in Nm')
