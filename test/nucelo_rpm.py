#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Testing the Nucleo.
In this program the return values of the nucleus can be viewed.
"""

import serial
import io

OUTPUT_MODE = "31"                                      # Input: A0, A1, A2; Frequency: 100Hz; Low pass filter: On

usb = serial.Serial('COM3', 115200, timeout=2)
usb.reset_output_buffer()
usb.flushOutput()
usb.flush()
nucleo = io.TextIOWrapper(io.BufferedRWPair(usb, usb))

nucleo.write(OUTPUT_MODE + "\n")                        # Start
nucleo.flush()


try:
    while True:
        data = nucleo.readline()
        split_data = data.split(' ')
        print(split_data)

except KeyboardInterrupt:                               # Exit
    nucleo.write("\n")
    nucleo.flush()
    usb.close()
