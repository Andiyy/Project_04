# -*- coding: utf-8 -*-

""""""


from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
import numpy as np
import serial
import io
from threading import Thread
import time


class RunProgram:
    """"""

    def __init__(self, data):
        self.data = data

        self.factory = PiGPIOFactory(host='192.168.2.135')
        self.relay_up = LED(23, pin_factory=self.factory)
        self.relay_down = LED(24, pin_factory=self.factory)

        self._steps = self.data.new_measurement.h_length * 100 + 100

        # Raw data:
        self.raw_current = np.zeros(self._steps)
        self.raw_voltage = np.zeros(self._steps)
        self.raw_rpm = np.zeros(self._steps)
        self.bit_rpm = np.zeros(self._steps)

        # Final data:
        self.current = np.zeros(self._steps)
        self.voltage = np.zeros(self._steps)
        self.rpm = []
        self.frequency = np.arange(0, self._steps, 50)
        self.time = np.arange(0, self.data.new_measurement.h_length, 0.01)
        self.time_rpm = [i/2 for i in range(0, self.data.new_measurement.h_length * 2, 1)]

        self._output_mode = self._nucleo_output_mode(analog_input=3, frequency=3, low_pass_filter=True)

    def run_program(self):
        """Running the Program."""
        usb = serial.Serial('COM3', 115200, timeout=2)
        nucleo = io.TextIOWrapper(io.BufferedRWPair(usb, usb))
        thread_relays = Thread(target=self._start, args=(self.data.new_measurement.h_length,))

        nucleo.write(str(self._output_mode) + "\n")
        nucleo.flush()
        thread_relays.start()

        for i in range(self._steps):
            data = nucleo.readline()
            split_data = data.split(' ')

            self.raw_current[i] = int(split_data[0])
            self.raw_voltage[i] = int(split_data[1])
            self.raw_rpm[i] = int(split_data[2])

        nucleo.write("\n")
        nucleo.flush()
        usb.close()

        self._update_values()

    def _start(self, duration: int):
        """Starting the motor."""
        time.sleep(0.5)
        self.relay_up.on()
        time.sleep(duration)
        self.relay_up.off()

    def _update_values(self):
        """Updating the values."""
        for index, element in enumerate(self.raw_current):
            self.current[index] = (element - 2904.99) * 0.000805664 / 0.185  # Offset: 2904.9977153301347

        for index, element in enumerate(self.raw_voltage):
            self.voltage[index] = element * 0.000805664 / 0.195

        for index, element in enumerate(self.raw_rpm):
            value = element * 0.000805664

            if value > 1.65:
                self.bit_rpm[index] = 1

        counter = 0

        try:
            for index, element in enumerate(self.bit_rpm):
                if element == 1 and self.bit_rpm[index + 1] == 0:
                    counter += 1

                if index in self.frequency:
                    current_rpm = counter/6
                    self.rpm.append(current_rpm)
                    counter = 0

        except IndexError:
            pass

        self.data.measured_values['Current'] = self.current
        self.data.measured_values['Voltage'] = self.voltage
        self.data.measured_values['RPM'] = self.rpm

    @staticmethod
    def _nucleo_output_mode(analog_input: (1, 2, 3), frequency: (1, 2, 3, 4), low_pass_filter=True) -> int:
        """Setting up the nucleo output mode.

        :param analog_input:    1 -> A0
                                2 -> A0, A1
                                3 -> A0, A1, A2
        :param frequency:       1 -> 1Hz
                                2 -> 10Hz
                                3 -> 100Hz
                                4 -> 1000Hz
        :param low_pass_filter: True  -> On
                                False -> Off

        :return Integer for the output mode.
        """
        if low_pass_filter:
            return 10 * analog_input + frequency
        elif not low_pass_filter:
            return - 10 * analog_input + frequency
