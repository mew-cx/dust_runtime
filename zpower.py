# https://learn.adafruit.com/adafruit-esp32-s2-feather/i2c-power-management

import time
import board
import digitalio

i2c_power = digitalio.DigitalInOut(board.I2C_POWER)
i2c_power.switch_to_input()
print("DISABLE")

time.sleep(0.01)  # wait for value to settle
rest_level = i2c_power.value
i2c_power.switch_to_output(value=(not rest_level))
print("ENABLE")

