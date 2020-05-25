import time
#from multiprocessing import Process, Queue, Pipe
import sqlite3 as sql

import matplotlib.pyplot as plt

import board
import busio
i2c = busio.I2C(board.SCL, board.SDA)
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
ads = ADS.ADS1115(i2c) #, data_rate=860
GAIN = 2/3

# current Sens / Channel 0
chan2 = AnalogIn(ads, ADS.P2)

# voltage / Channel 2
chan3 = AnalogIn(ads, ADS.P3)

# Spannungswerte
y1 = []

# Stromwerte
y2 = []

# Zeit
x = []
time_program = 0

def read_u():
    """Get the actual voltage value."""
    spannung = (chan3.voltage * 3)
    #y1.append(spannung)
    print(f"Spannung: {spannung}")
    #return voltage.voltage * 3  # Voltage Divider!


def read_i():

    """Get the actual current value."""
    
    strom = (chan2.voltage) * 1000
    #stromL1= (chan0.voltage / 65535) * 5000
    #stromA1 = (chan1.voltage / 65535) * 5000
    stromL = (strom - 2585) / 187.5
    #stromA1_A = (stromA -2530) / 187.5
    
    #/ 0.1875
    #y2.append(strom)
    #vout2 = chan0.voltage
    #strom2 = ((((vout2 - 13653) * 0.1875) * 1.612) / 100)
    #strom = '%.2f' % (chan2.voltage -2.5)
    print(f"Spannungswert_L:    {strom}")
    print(f"Spannungswert_L1:    {stromL}")
    #print(f"Spannungswert_A1:    {stromA1_A}")
    #print(f"Spannungvout2:    {vout2}")
    #print(f"Stromumrechnung:    {strom}")
    #print(f"Strom2:    {strom2}")

    #return 10 * (current.voltage - 2.5)  # 10A/V * (U - 2,5V)


def main():
    """Start the dirfferent processes.

    Set the duration for the measurement and start
    the processes in the required order."""
    global x, y1, y2, time_program
        
    
    while True:
        
        #u = read_u()
        #i = read_i()
        #print(f"Spannung: {u}")
        #print(f"Strom:    {i}")
        #print(current)
        #print(voltage)
        print("------------------------------------")
        x.append(time_program)
        read_u()
        read_i()
        a = 0.01
        time.sleep(a)
        time_program += a
        

if __name__ == "__main__":
    try:
        main()
        
    except KeyboardInterrupt:
        
        plt.subplot(2, 1, 1)
        plt.plot(x, y2, 'o-')
        plt.title('Strom-Zeit-Diagramm')
        plt.xlabel('Zeit in s')
        plt.ylabel('Strom in A')

        plt.subplot(2, 1, 2)
        plt.plot(x, y1, 'o-')
        plt.title('Spannung-Zeit-Diagramm')
        plt.xlabel('Zeit in s')
        plt.ylabel('Spannung in V')

        plt.show()
        print(f"Zeit:{x}")
        print(f"Spannung:{y1}")
        print(f"Strom:{y2}")
        #GPIO.cleanup()