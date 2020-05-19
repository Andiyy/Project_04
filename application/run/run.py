# import matplotlib.pyplot as plt
# import time
# import numpy as np
#
# import board
# import busio
# import adafruit_ads1x15.ads1115 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn
#
#
# i2c = busio.I2C(board.SCL, board.SDA)
# ads = ADS.ADS1115(i2c, data_rate=860)
#
# # current / Channel 2
# chan2 = AnalogIn(ads, ADS.P2)
#
# # voltage / Channel 3
# chan3 = AnalogIn(ads, ADS.P3)
#
#
# class RunProgram:
#     """"""
#
#     def __init__(self, time_step):
#         # Time/Steps:
#         self._time_step = time_step
#         self._amount_steps = int(10 / self._time_step + 1)
#         self._current_step = 0
#
#         # Creating the arrays:
#         self._y_voltage = np.zeros(self._amount_steps)
#         self._y_current = np.zeros(self._amount_steps)
#         self._x_time = np.arange(0, 5.001, self._time_step)
#
#         self._data = {'Voltage': self._y_voltage, 'Current': self._y_current, 'Time': self._x_time}
#
#     def return_values(self) -> dict:
#         """Returning the dictionary."""
#         return self._data
#
#     def write_values(self, filename):
#         """Writing the data into a .csv-file.
#
#         :param filename    The filename of the csv.-file.
#         """
#         with open(f'{filename}.csv', 'w') as file:
#
#             for item_list in self._data:
#                 for item in self._data[f'{item_list}']:
#                     file.write(f'{item};')
#                 file.write('\n')
#
#     def run_program(self):
#         """Running the Program."""
#         for current_step in range(self._amount_steps):
#             # Current:
#             current = (chan2.voltage / 4095) * 5000
#             self._y_current[current_step] = current
#
#             # Voltage:
#             voltage = chan3.voltage * 3
#             self._y_voltage[current_step] = voltage
#
#             time.sleep(self._time_step)
#
#
# def get_user_input() -> (float, str):
#     """Getting the user input."""
#     while True:
#         try:
#             time_step = input('Time steps: ')
#             filename = input('Filename: (Without <.csv>)')
#             return float(time_step), filename
#         except ValueError:
#             print('Wrong input! You have to input a int or a float!')
#
#
# def main():
#     """"""
#     time_step, filename = get_user_input()
#     run_class = RunProgram(time_step=time_step)
#
#     run_class.run_program()
#
#     plot_data(data=run_class.return_values())
#     if filename != '':
#         run_class.write_values(filename=filename)
#
#
# def plot_data(data: dict):
#     """Showing the data in a plot."""
#     plt.subplot(2, 1, 1)
#     plt.plot(data['Time'], data['Current'], 'o-')
#     plt.title('Strom-Zeit-Diagramm')
#     plt.xlabel('Zeit in s')
#     plt.ylabel('Strom in A')
#
#     plt.subplot(2, 1, 2)
#     plt.plot(data['Time'], data['Voltage'], 'o-')
#     plt.title('Spannung-Zeit-Diagramm')
#     plt.xlabel('Zeit in s')
#     plt.ylabel('Spannung in V')
#
#     plt.show()
#
#
# if __name__ == '__main__':
#     main()
