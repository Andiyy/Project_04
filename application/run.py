# -*- coding: utf-8 -*-

"""Measurement."""

from PyQt5 import QtWidgets
from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
import numpy as np
import serial
import io
from threading import Thread
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class RunProgram:
    """Stating the measurement and storing the data."""

    def __init__(self, data, main_window):
        self.data = data
        self.main_window = main_window

        self._initialize_pi()
        self._initialize_nucleo_output_mode(analog_input=3, frequency=3, low_pass_filter=True)
        self._raw_data()

    def _initialize_pi(self):
        """Initialize Raspberry Pi."""
        self.factory = PiGPIOFactory(host=self.data.raspberry_pi.ip)
        self.relay_up = LED(23, pin_factory=self.factory)
        self.relay_down = LED(24, pin_factory=self.factory)

    def _initialize_nucleo_output_mode(self, analog_input: (1, 2, 3), frequency: (1, 2, 3, 4), low_pass_filter=True):
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

        The low pass filter can only be active if the frequency is less or equal to 3
        """
        if low_pass_filter and frequency == 4:
            raise ValueError('The low pass filter can only be active if the frequency is less or equal to 3')

        if low_pass_filter:
            self._output_mode = str(10 * analog_input + frequency)
        elif not low_pass_filter:
            self._output_mode = str(-10 * analog_input + frequency)

    def _raw_data(self):
        """Creating the Arrays.

        steps:          *100 -> 100Hz Nucleo
                        +200 -> 1 Seconds idle at start and the end.
        """
        self._steps = self.data.new_measurement.h_length * 100 + 200

        self.raw_rpm = np.zeros(self._steps)
        self.bit_rpm = np.zeros(self._steps)

        # Final data:
        self.time = np.arange(0, self.data.new_measurement.h_length + 2, 0.01)
        self.current = np.zeros(self._steps)
        self.voltage = np.zeros(self._steps)
        self.rpm = []
        self.frequency = np.arange(0, self._steps, 50)

    def _live_plot_update(self, _):
        """Updating the live plot data.
        Can only be called by the method _live_plot!
        """
        plt.cla()
        plt.plot(self.time, self.current, label='Current')
        plt.plot(self.time, self.voltage, label='Voltage')
        plt.legend(loc='upper right')
        plt.tight_layout()

    def _live_plot(self):
        """THREAD: Creating the live plot.
        The graphic is updated every second.
        """
        import seaborn as sns

        sns.set_style('whitegrid')

        animation = FuncAnimation(plt.gcf(), self._live_plot_update, interval=1000)
        plt.show()
        plt.close()

    def run_program(self) -> bool:
        """Running the Program.
        First the serial port and the connected Nucleo are set up.
        The motor control is started in another thread. This runs simultaneously with the readout of the measurement
        data.
        Et the end the the Nucleo is stopped and the port is closed.
        """
        thread_animate = Thread(target=self._live_plot, args=())
        thread_animate.start()

        usb = serial.Serial(self.data.nucleo, 115200, timeout=2)
        usb.reset_output_buffer()
        usb.flushOutput()
        usb.flush()
        nucleo = io.TextIOWrapper(io.BufferedRWPair(usb, usb))
        thread_relays = Thread(target=self._start, args=(self.data.new_measurement.h_length, ))

        # Starting the Nucleo and the thread:
        nucleo.write(str(self._output_mode) + "\n")
        nucleo.flush()
        thread_relays.start()

        try:
            for i in range(self._steps):
                data = nucleo.readline()
                split_data = data.split(' ')

                self.current[i] = (int(split_data[0]) - 2836) * 0.000805664 / 0.185
                self.voltage[i] = int(split_data[1]) * 0.000805664 / 0.195
                self.raw_rpm[i] = int(split_data[2])

        except ValueError:                  # Sometime the Nucleo returns invalid data
            self.relay_up.off()
            message = QtWidgets.QMessageBox()
            message.warning(self.main_window, 'Warning', 'The Nucleo has sent an invalid value. Please check the '
                                                         'connection and press the reset button if necessary!')
            return False

        finally:                            # Resetting the Nucleo
            nucleo.write("\n")
            nucleo.flush()
            usb.close()
            self.factory.close()

        self._update_values()
        return True

    def _start(self, duration: int):
        """THREAD: Starting the motor."""
        time.sleep(1)
        self.relay_up.on()
        time.sleep(duration)
        self.relay_up.off()

    def _update_values(self):
        """Updating the values."""
        for index, element in enumerate(self.raw_rpm):
            if element > 2100:
                self.bit_rpm[index] = 1

        counter = 0

        try:
            for index, element in enumerate(self.bit_rpm):
                if element == 1 and self.bit_rpm[index + 1] == 0:
                    counter += 1

                if index in self.frequency:

                    if index == 50 or index == 100:
                        self.rpm.append(0)
                    else:
                        current_rpm = counter / 12
                        self.rpm.append(current_rpm * 120)
                        counter = 0

        except IndexError:              # If the last entry is a 1
            pass

        self.data.measured_values['Current'] = self.current
        self.data.measured_values['Voltage'] = self.voltage
        self.data.measured_values['RPM'] = self.rpm

        # self._show_raw_rpm()          # Showing the raw rpm data.

    def _show_raw_rpm(self):
        """Showing the rpm signal as diagram.

        NOT USED!
        You can coll the method at the end of the _update_values method."""
        import seaborn as sns

        fig, ax = plt.subplots()

        fig.dpi = 100

        sns.set_style('whitegrid')

        x_time = np.arange(0, self.data.new_measurement.h_length + 2, 0.01)

        ax.plot(x_time, self.raw_rpm)

        ax.set_xlabel('Time in s')
        ax.set_ylabel('RPM in 1/min')

        ax.grid()
        plt.show()

        fig.savefig(f'{str(time.time()).replace(".", "_")}.png', transparent=True)
