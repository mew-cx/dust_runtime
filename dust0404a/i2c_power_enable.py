import time
import digitalio
import board

def I2c_power_enable(enable):
    i2c_power = digitalio.DigitalInOut(board.I2C_POWER)
    i2c_power.switch_to_input()
    if enable:
        time.sleep(0.01)  # wait for default value to settle
        rest_level = i2c_power.value
        i2c_power.switch_to_output(value=(not rest_level))
