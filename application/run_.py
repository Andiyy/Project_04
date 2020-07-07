# -*- coding: utf-8 -*-

""""""


import RPi.GPIO as GPIO
import numpy as np
import serial
import io


class RunProgram:
    RELAY1 = 23
    RELAY2 = 24

    """"""
    def __init__(self, data):
        self.data = data

        self._steps = self.data.new_measurement.h_length * 100

        # Raw data:
        self.raw_current = np.zeros(self._steps)
        self.raw_voltage = np.zeros(self._steps)
        self.raw_rpm = np.zeros(self._steps)
        self.bit_rpm = np.zeros(self._steps)

        # Final data:
        self.current = np.zeros(self._steps)
        self.voltage = np.zeros(self._steps)
        self.rpm = []
        self.frequency = [i for i in range(0, self.data.new_measurement.h_length * 100, 50)]
        self.time = np.arange(0, self.data.new_measurement.h_length, 0.01)
        self.time_rpm = [i/2 for i in range(0, self.data.new_measurement.h_length * 2, 1)]

        self._output_mode = self._nucleo_output_mode(analog_input=3, frequency=3, low_pass_filter=True)

        self._setup_pi()

    def _setup_pi(self):
        """Setup for the GPIOs."""
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.RELAY1, GPIO.OUT)
        GPIO.setup(self.RELAY2, GPIO.OUT)
        GPIO.output(self.RELAY1, GPIO.LOW)
        GPIO.output(self.RELAY2, GPIO.LOW)

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

    @staticmethod
    def run(relay: ('RELAY1', 'RELAY2'), mode: bool = False):
        """Turning the relays on and off.

        :param relay    Relay1 or Relay2
        :param mode     On/Off
        """
        if mode:
            mode = GPIO.HIGH
        elif not mode:
            mode = GPIO.LOW
        else:
            raise ValueError('You have to enter a bool!')

        GPIO.output(relay, mode)

    def run_program(self):
        """Running the Program."""
        usb = serial.Serial('/dev/ttyACM0', 115200, timeout=2)
        nucleo = io.TextIOWrapper(io.BufferedRWPair(usb, usb))

        nucleo.write(str(self._output_mode) + "\n")
        nucleo.flush()

        self.run(self.RELAY1, True)

        for i in range(self._steps):
            data = nucleo.readline()
            split_data = data.split(' ')

            self.raw_current[i] = int(split_data[0])
            self.raw_voltage[i] = int(split_data[1])
            self.raw_rpm[i] = int(split_data[2])

        self.run(self.RELAY1, False)

        nucleo.write("\n")
        nucleo.flush()
        usb.close()

        self._update_values()

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
                if element == 1 and self.bit_rpm[index + 1] is 0:
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


        # fig = plt.figure()
        #
        # current = fig.add_subplot(2, 1, 1)
        # plt.plot(self.time, self.current, '.-')
        # plt.xlabel('Seconds')
        # plt.ylabel('Current in A')
        #
        # plt.subplot(2, 1, 2)
        # plt.plot(self.time, self.voltage, '.-')
        # plt.xlabel('Seconds')
        # plt.ylabel('Voltage in V')

        # plt.subplot(4, 1, 3)
        # plt.plot(self.time, self.raw_rpm, '.-')
        # plt.xlabel('Seconds')
        # plt.ylabel('RPM - Signal')
        #
        # plt.subplot(4, 1, 4)
        # plt.plot(self.frequency, self.rpm, '.-')
        # plt.xlabel('Seconds')
        # plt.ylabel('RPM')
        #
        # plt.show()

        # import matplotlib.pyplot as plt
        #
        # fig = plt.figure(figsize=(6, 4))
        #
        # sub1 = fig.add_subplot(221)
        # sub1.set_title('Current - Time')
        # sub1.plot(self.time, self.current)
        #
        # sub2 = fig.add_subplot(222)
        # sub2.set_title('Voltage - Time')
        # sub2.plot(self.time, self.voltage)
        #
        # sub3 = fig.add_subplot(223)
        # sub3.set_title('RPM Signal')
        # sub3.plot(self.time, self.raw_rpm)
        #
        # sub4 = fig.add_subplot(224)
        # sub4.set_title('RPM - Time')
        # sub4.plot(self.frequency, self.rpm)
        #
        # plt.tight_layout()
        # plt.show()


def clear():
    """Clearing the GPIOs and turning of the relays."""
    try:
        relay_1 = 23
        relay_2 = 24

        GPIO.output(relay_1, GPIO.LOW)
        GPIO.output(relay_2, GPIO.LOW)

        GPIO.cleanup()

    except RuntimeError:
        pass
