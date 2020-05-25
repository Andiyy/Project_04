import time

# Import the ADS1x15 module.
import Adafruit_ADS1x15 as ADS

# Create an ADS1115 ADC (16-bit) instance.
#adc = Adafruit_ADS1x15.ADS1115()
adc = ADS.ADS1115()

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()


# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1


# current SensLadi / Channel 0
chan0 = adc.read_adc(0, gain=GAIN)
# current SensAndi / Channel 1
chan1 = adc.read_adc(1, gain=GAIN)
# voltage / Channel 2
chan2 = adc.read_adc(2, gain=GAIN)

def read_u():
    """Get the actual voltage value."""
    spannung = (chan2 * 3)
    #y1.append(spannung)
    print(f"Spannung: {spannung}")
    #return voltage.voltage * 3  # Voltage Divider!

def read_i():

    """Get the actual current value."""
    vout = (chan0 / 65535) * 5000
    
    stromL = (chan0)
    stromA = (chan1)
    stromL_V = (chan0 / 4) / 2
    stromL1 = (chan0 / 65535) * 5000
    stromA1 = (chan1 / 65535) * 5000
    stromL1_AV = (stromL1 - 2570) / 185
    stromL1_A = (stromL1 - 2500) / 185
    stromA1_A = (stromA1 - 2500) / 185

    print(f"Spannungswert_L:    {stromL}")
    print(f"Spannungswert_L_V:    {stromL_V}")
    print(f"Spannungswert_L1_AV:    {stromL1_AV}")
    print(f"Spannungswert_A:    {stromA}")
    print(f"Spannungswert_L1:    {stromL1}")
    print(f"Spannungswert_A1:    {stromA1}")
    print(f"Spannungswert_L1:    {stromL1_A}")
    print(f"Spannungswert_A1:    {stromA1_A}")
    
    
def main():
    
    while True:
        
        print("------------------------------------")
        read_u()
        read_i()
        a = 0.5
        time.sleep(a)
        
if __name__ == "__main__":
    main()


