#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  6 20:37:27 2018
@author: user
"""

import serial
import io
import matplotlib.pyplot as plt


def nucleo_output_mode(analog_input, frequency, low_pass_filter=True) -> int:
    """"""
    if low_pass_filter:
        return 10 * analog_input + frequency
    elif not low_pass_filter:
        return - 10 * analog_input + frequency


OUTPUT_MODE = nucleo_output_mode(3, 3, True)

raw_current = []
raw_voltage = []
raw_rpm = []
rpm_bit = []

current = []
voltage = []
rpm_values = []
rpm = []


usb = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
nucleo = io.TextIOWrapper(io.BufferedRWPair(usb, usb))

nucleo.write(str(OUTPUT_MODE) + "\n")
nucleo.flush()


for _ in range(1000):
    data = nucleo.readline()
    split_data = data.split(' ')

    raw_current.append(int(split_data[0]))
    raw_voltage.append(int(split_data[1]))
    raw_rpm.append(int(split_data[2]))

nucleo.write("\n")
nucleo.flush()
usb.close()

for element in raw_current:
    current.append((int(element) - 2904.99) * 0.000805664 / 0.185)
    # Offset: 2904.9977153301347

for element in raw_voltage:
    voltage.append(int(element) * 0.000805664 / 0.195)
    # 12V -> 0.1951721502
    # 06V -> 0.1913102134

for element in raw_rpm:
    value = int(element) * 0.000805664
    rpm_values.append(value)
    if value > 1.65:
        rpm_bit.append(True)
    else:
        rpm_bit.append(False)

counter = 0
frequency = [i for i in range(50, 1050, 50)]
print(frequency)

rpm.append(0)

try:
    for index, element in enumerate(rpm_bit):
        if element is True and rpm_bit[index + 1] is False:
            counter += 1

        if index in frequency:
            current_rpm = counter / 6
            rpm.append(current_rpm)
            counter = 0

except IndexError:
    pass

x = [i/100 for i in range(len(current))]
x_rpm = [i/2 for i in range(0, 20, 1)]

plt.subplot(4, 1, 1)
plt.plot(x, current, '.-')
plt.xlabel('Seconds')
plt.ylabel('Current in A')

plt.subplot(4, 1, 2)
plt.plot(x, voltage, '.-')
plt.xlabel('Seconds')
plt.ylabel('Voltage in V')

plt.subplot(4, 1, 3)
plt.plot(x, rpm_values, '.-')
plt.xlabel('Seconds')
plt.ylabel('RPM - Signal')

plt.subplot(4, 1, 4)
plt.plot(x_rpm, rpm, '.-')
plt.xlabel('Seconds')
plt.ylabel('RPM')

plt.show()
