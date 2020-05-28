import time
import numpy as np
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import RPi.GPIO as GPIO


class RunProgram:
    # AD:
    I2C = busio.I2C(board.SCL, board.SDA)
    ADS_I2C = ADS.ADS1115(I2C)
    # ADC = ADS.ADS1115()
    CHAN2 = AnalogIn(ADS_I2C, ADS.P2)  # current / Channel 2
    CHAN3 = AnalogIn(ADS_I2C, ADS.P3)  # voltage / Channel 3
    GAIN = 1

    # Relays:
    RELAY1 = 23
    RELAY2 = 24

    """"""

    def __init__(self, time_step):
        # Time/Steps:
        self._time_step = time_step
        self._amount_steps = int(10 / self._time_step + 1)
        self._current_step = 0

        # Creating the arrays:
        self._y_voltage = np.zeros(self._amount_steps)
        self._y_current = np.zeros(self._amount_steps)
        self._x_time = np.arange(0, 5.001, self._time_step)

        self._data = {'Voltage': self._y_voltage, 'Current': self._y_current, 'Time': self._x_time}

    def setup_pi(self):
        """Setup for the GPIOs."""
        GPIO.setmode(GPIO.BOARD)
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

    def destroy(self):
        """Raspberry Pi output on LOW."""
        GPIO.output(self.RELAY1, GPIO.LOW)
        GPIO.output(self.RELAY2, GPIO.LOW)
        GPIO.cleanup()

    def return_values(self) -> dict:
        """Returning the dictionary."""
        return self._data

    def run_program(self):
        """Running the Program."""
        start = time.time()
        for current_step in range(self._amount_steps):
            # Current:
            current = (self.CHAN2.voltage / 4095) * 5000
            self._y_current[current_step] = current

            # Voltage:
            voltage = self.CHAN3.voltage * 3
            self._y_voltage[current_step] = voltage

            time.sleep(self._time_step)

        print(start-time.time())


test = RunProgram(1)
test.run(test.RELAY1, True)
time.sleep(1)
test.run(test.RELAY1, False)

time.sleep(2)

test.run(test.RELAY2, True)
time.sleep(1)
test.run(test.RELAY2, False)
