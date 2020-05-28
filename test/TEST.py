import matplotlib.pyplot as plt
import time
import numpy as np
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO
from multiprocessing import Process, Manager


class RunProgram:
    # AD:
    I2C = busio.I2C(board.SCL, board.SDA)
    _ADS = ADS.ADS1115(I2C)
    # ADC = ADS.ADS1115()
    CHAN2 = AnalogIn(_ADS, ADS.P2)  # current / Channel 2
    CHAN3 = AnalogIn(_ADS, ADS.P3)  # voltage / Channel 3
    GAIN = 1

    # Relays:
    RELAY1 = 23
    RELAY2 = 24

    """"""

    def __init__(self, time_step):
        # Time/Steps:
        self._time_step = time_step
        self._amount_steps = int(5 / self._time_step + 1)
        self._current_step = 0
        self._rpm = 0

        # Creating the arrays:
        self._y_voltage = np.zeros(self._amount_steps)
        self._y_current = np.zeros(self._amount_steps)
        self._x_time = np.arange(0, 5.001, self._time_step)

        self._data = {'Voltage': self._y_voltage, 'Current': self._y_current, 'Time': self._x_time}

        self._setup_pi()

    def _setup_pi(self):
        """Setup for the GPIOs."""
        # Relays: 
        GPIO.setup(self.RELAY1, GPIO.OUT)
        GPIO.setup(self.RELAY2, GPIO.OUT)
        GPIO.output(self.RELAY1, GPIO.LOW)
        GPIO.output(self.RELAY2, GPIO.LOW)

        # RPM: 
        GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(17, GPIO.FALLING, bouncetime=25)

    @staticmethod
    def turn(relay, mode: bool = False):
        """Turning the relays on and off.

        :param relay    Relay
        :param mode     On/Off
        """
        if mode:
            mode = GPIO.HIGH
        elif not mode:
            mode = GPIO.LOW
        else:
            raise ValueError('You have to enter a bool!')

        GPIO.output(relay, mode)

    def _destroy(self):
        """Raspberry Pi output on LOW."""
        GPIO.output(self.RELAY1, GPIO.LOW)
        GPIO.output(self.RELAY2, GPIO.LOW)
        GPIO.cleanup()

    def return_values(self) -> dict:
        """Returning the dictionary."""
        return self._data

    def thread_cur_vol(self):
        """"""

    def thread_rpm(self):
        """"""

    def run_program(self):
        """Running the Program."""
        self.turn(23, True)

        for current_step in range(self._amount_steps):
            # Current:
            current_voltage = (self.CHAN2.voltage) * 1000
            current = (current_voltage - 2585) / 187.5
            self._y_current[current_step] = current

            # Voltage:
            voltage = self.CHAN3.voltage * 3
            self._y_voltage[current_step] = voltage

            if GPIO.event_detected(17):
                self._rpm += 1
                print(self._rpm)

            time.sleep(self._time_step)

        self.turn(23, False)

        time.sleep(1)

        self.turn(24, True)
        time.sleep(4.4)
        self.turn(24, False)
        self._destroy()


test = RunProgram(1)
test.run_program()

a = test.return_values
