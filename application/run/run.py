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
    ADS_I2C = ADS.ADS1115(I2C)
    # ADC = ADS.ADS1115()
    CHAN2 = AnalogIn(ADS_I2C, ADS.P2)  # current / Channel 2
    CHAN3 = AnalogIn(ADS_I2C, ADS.P3)  # voltage / Channel 3
    GAIN = 1

    # Relays:
    RELAY1 = 23
    RELAY2 = 24

    """"""

    def __init__(self, data):
        self.data = data

        # Time/Steps:
        self._amount_steps = int(5 / self.data.new_measurement.h_step + 1)

        # Creating the arrays:
        self._y_voltage = None
        self._y_current = None
        self._y_rpm = None
        self._x_time = np.arange(0, 5.001, self.data.new_measurement.h_step)

        self.data.measured_values = {'Voltage': self._y_voltage, 'Current': self._y_current, 'Time': self._x_time,
                                     'RPM': self._y_rpm}

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

    def destroy(self):
        """Raspberry Pi output on LOW."""
        GPIO.output(self.RELAY1, GPIO.LOW)
        GPIO.output(self.RELAY2, GPIO.LOW)
        GPIO.cleanup()

    def _process_voltage(self, queue):
        """"""
        print('Voltage, Start')

        y_voltage = np.zeros(self._amount_steps)
        for step in range(self._amount_steps):
            voltage = self.CHAN3.voltage * 3
            y_voltage[step] = voltage
            # time.sleep(self.data.new_measurement.h_step)

        queue.put(y_voltage)
        print(y_voltage)
        print('Voltage, Finish')

    def _process_current(self, queue):
        """"""
        print('Current, Start')
        y_current = np.zeros(self._amount_steps)
        for step in range(self._amount_steps):
            current_voltage = self.CHAN2.voltage * 1000
            current = (current_voltage - 2585) / 187.5
            y_current[step] = current
            # time.sleep(self.data.new_measurement.h_step)

        queue.put(y_current)
        print(y_current)
        print('Current, Finish')

    def _process_rpm(self, queue):
        """"""
        print('RPM, Start')
        a = 0
        a += 1
        queue.put(a)
        time.sleep(10)
        print('RPM, Finish')

    def run_program(self):
        """Running the Program."""
        q_voltage = Queue()
        q_current = Queue()
        q_rpm = Queue()

        p_voltage = Process(target=self._process_voltage, args=(q_voltage,))
        p_current = Process(target=self._process_current, args=(q_current,))
        p_rpm = Process(target=self._process_rpm, args=(q_rpm,))

        p_voltage.start()
        p_current.start()
        p_rpm.start()
        start = time.time()
        self.run(self.RELAY1, True)

        self._y_voltage = q_voltage.get()
        self._y_current = q_current.get()
        self._y_rpm = q_rpm.get()

        p_voltage.join()
        p_current.join()
        p_rpm.kill()

        self.run(self.RELAY1, False)
        print(f'Time: {time.time()-start}')

        time.sleep(1)
        self.run(self.RELAY2, True)
        time.sleep(3)
        self.run(self.RELAY2, False)

        print(self._y_voltage)
        print(self._y_current)
        print(self._y_rpm)
