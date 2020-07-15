# -*- coding: utf-8 -*-

"""Old measuring program!
For use, the corresponding modules must be installed and the structure must be adapted. Furthermore, this program must
be executed on the Raspberry Pi.

Without Nucleo.

The program is for documentation purposes only!!!
"""

import time
import numpy as np
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
from multiprocessing import Process, Queue


class RunProgram:
    # AD:
    I2C = busio.I2C(board.SCL, board.SDA)
    ADS_I2C = ADS.ADS1115(I2C, gain=1)
    CHAN1 = AnalogIn(ADS_I2C, ADS.P1)  # rpm     / Channel 1
    CHAN2 = AnalogIn(ADS_I2C, ADS.P2)  # current / Channel 2
    CHAN3 = AnalogIn(ADS_I2C, ADS.P3)  # voltage / Channel 3

    # Relays:
    RELAY1 = 23
    RELAY2 = 24

    """"""
    def __init__(self, data):
        self.data = data

        # Time/Steps:
        self._step = 0.0221
        self._amount_steps = int(self.data.new_measurement.h_length / self._step + 1)

        self.data.measured_values = {'Voltage': None,
                                     'Current': None,
                                     'Time': np.arange(0, self.data.new_measurement.h_length, self._step),
                                     'RPM': None}

        self._setup_pi()

    def _setup_pi(self):
        """Setup for the GPIOs."""
        GPIO.setup(self.RELAY1, GPIO.OUT)
        GPIO.setup(self.RELAY2, GPIO.OUT)
        GPIO.output(self.RELAY1, GPIO.LOW)
        GPIO.output(self.RELAY2, GPIO.LOW)

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

    def _process_voltage_current(self, queue_v, queue_c):
        """"""
        y_voltage = np.zeros(self._amount_steps)
        y_current = np.zeros(self._amount_steps)

        for step in range(self._amount_steps):
            y_voltage[step] = self.CHAN3.value
            y_current[step] = self.CHAN2.value

        queue_v.put(y_voltage)
        queue_c.put(y_current)

    def _process_rpm(self, queue):
        """"""
        y_rpm = np.zeros(self._amount_steps)

        start = time.time()

        for step in range(self._amount_steps):
            y_rpm[step] = self.CHAN1.value

        print(f'Time RPM: {time.time() - start}')

        queue.put(y_rpm)

    def run_program(self):
        """Running the Program."""
        q_voltage = Queue()
        q_current = Queue()
        q_rpm = Queue()

        p_voltage_current = Process(target=self._process_voltage_current, args=(q_voltage, q_current))
        p_rpm = Process(target=self._process_rpm, args=(q_rpm,))

        p_voltage_current.start()
        p_rpm.start()

        time.sleep(0.05)
        self.run(self.RELAY1, True)

        p_voltage_current.join()
        p_rpm.join()

        self.data.measured_values['Voltage'] = q_voltage.get()
        self.data.measured_values['Current'] = q_current.get()
        self.data.measured_values['RPM'] = q_rpm.get()

        self._update_values()

        self.run(self.RELAY1, False)

    def _update_values(self):
        """Updating the values."""
        bit_current = 20288

        for index, value in enumerate(self.data.measured_values['Voltage']):
            self.data.measured_values['Voltage'][index] = value * 0.0006226

        for index, value in enumerate(self.data.measured_values['Current']):
            self.data.measured_values['Current'][index] = (value - bit_current) * 0.125 / 185

        counter = 0
        test = []
        try:
            for index, element in enumerate(self.data.measured_values['RPM']):
                if element >= 24_000:
                    test.append(True)
                else:
                    test.append(False)

            for index, element in enumerate(test):
                if element is True and test[index+1] is False:
                    counter += 1
        except IndexError:
            print(f'Zähler: {counter}')

        print(f'Zähler: {counter}')


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
