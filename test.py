import numpy as np
import matplotlib.pyplot as plt

from database.database import open_sqlite3

time = np.arange(0, 8.5, 0.01)

current_1 = np.zeros(850)
voltage_1 = np.zeros(850)
power_1 = np.zeros(850)

current_2 = np.zeros(850)
voltage_2 = np.zeros(850)
power_2 = np.zeros(850)

current_3 = np.zeros(850)
voltage_3 = np.zeros(850)
power_3 = np.zeros(850)


def get_data(array, h_id, s_id):
    """"""
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


def calculate_power(array_current, array_voltage, array_power):
    """"""
    for index in range(len(array_power)):
        array_power[index] = array_current[index] * array_voltage[index]


calculate_power(current_1, voltage_1, power_1)
calculate_power(current_2, voltage_2, power_2)
calculate_power(current_3, voltage_3, power_3)


fig, ax = plt.subplots()
ax.plot(time, power_1)
ax.plot(time, power_2)
ax.plot(time, power_3)

ax.grid()
plt.show()







# x = np.arange(0, 5, 0.5)
# rpm = np.arange(0, 5, 0.5)
#
# power = np.arange(5, 10, 0.01)
# average_power = []  # np.zeros(int(len(power)/50))
# reset_counter = np.arange(0, len(power), 50)
#
# print(len(power))
# print(len(x))
#
# counter = 0
#
# for index, item in enumerate(power):
#     counter += item
#     if index in reset_counter:
#         counter /= 50
#         average_power.append(counter)
#         counter = 0
#
# fig, ax = plt.subplots()
# ax.plot(x, rpm)
# ax.plot(x, average_power)
#
# ax.grid()
# plt.show()
